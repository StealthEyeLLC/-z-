#!/usr/bin/env python3
"""Cloud Hypervisor v53.0 Unix-vsock mux connector.

This helper implements only the pinned mux preface (CONNECT <port>\n), then
passes the connected descriptor or relays opaque bytes. It never parses SSH.
"""
from __future__ import annotations

import argparse
import array
import errno
import hashlib
import json
import os
import select
import socket
import stat
import sys
from pathlib import Path

MAX_BUFFER_BYTES = 1024 * 1024


class Refusal(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_binding(path: Path) -> dict:
    st = path.lstat()
    if (
        stat.S_ISLNK(st.st_mode)
        or not stat.S_ISREG(st.st_mode)
        or st.st_uid != 0
        or stat.S_IMODE(st.st_mode) != 0o600
    ):
        raise Refusal("unsafe binding manifest")
    data = json.loads(path.read_text())
    if (
        data.get("schema_version") != "1.0.0"
        or data.get("protocol") != "cloud-hypervisor-v53-unix-vsock-mux"
    ):
        raise Refusal("binding schema/protocol mismatch")
    return data


def proc_start(pid: int) -> str:
    fields = Path(f"/proc/{pid}/stat").read_text().split()
    return fields[21]


def validate_socket(entry: dict, label: str) -> Path:
    path = Path(entry["path"])
    if not path.is_absolute() or ".." in path.parts:
        raise Refusal(f"{label} path invalid")
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISSOCK(st.st_mode):
        raise Refusal(f"{label} not a direct socket")
    if st.st_uid != 0 or st.st_gid != 0:
        raise Refusal(f"{label} not root-owned")
    for key, value in (
        ("uid", st.st_uid),
        ("gid", st.st_gid),
        ("dev", st.st_dev),
        ("ino", st.st_ino),
    ):
        if int(entry[key]) != value:
            raise Refusal(f"{label} identity mismatch: {key}")
    return path


def validate(binding: dict, port: int) -> Path:
    if port < 1 or port > 0xFFFFFFFF or port not in binding["allowed_ports"]:
        raise Refusal("port not allowed")
    pid = int(binding["vmm"]["pid"])
    if proc_start(pid) != str(binding["vmm"]["start_time"]):
        raise Refusal("VMM start identity mismatch")
    exe = Path(os.readlink(f"/proc/{pid}/exe"))
    if (
        str(exe) != binding["vmm"]["executable"]
        or sha256_file(exe) != binding["vmm"]["sha256"]
    ):
        raise Refusal("VMM executable mismatch")
    validate_socket(binding["api_socket"], "API socket")
    return validate_socket(binding["mux_socket"], "mux socket")


def connect_mux(path: Path, port: int) -> socket.socket:
    before = path.stat()
    stream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    stream.connect(str(path))
    after = path.stat()
    if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
        stream.close()
        raise Refusal("mux socket replaced during connect")
    if not stat.S_ISSOCK(os.fstat(stream.fileno()).st_mode):
        stream.close()
        raise Refusal("connected descriptor is not a socket")
    stream.sendall(f"CONNECT {port}\n".encode("ascii"))
    return stream


def fdpass(stream: socket.socket, wrong: bool = False) -> None:
    output = socket.socket(fileno=os.dup(1))
    try:
        descriptor = os.open("/dev/null", os.O_RDONLY) if wrong else stream.fileno()
        try:
            sent = output.sendmsg(
                [b"\0"],
                [
                    (
                        socket.SOL_SOCKET,
                        socket.SCM_RIGHTS,
                        array.array("i", [descriptor]),
                    )
                ],
            )
            if sent != 1:
                raise Refusal("descriptor transfer short write")
        finally:
            if wrong:
                os.close(descriptor)
    finally:
        output.close()


def relay(stream: socket.socket) -> None:
    """Relay opaque bytes with bounded buffers and exact half-close ordering."""
    stream.setblocking(False)
    os.set_blocking(0, False)
    os.set_blocking(1, False)

    to_stream = bytearray()
    to_stdout = bytearray()
    stdin_eof = False
    stream_eof = False
    stream_write_closed = False

    while True:
        if stdin_eof and not to_stream and not stream_write_closed:
            try:
                stream.shutdown(socket.SHUT_WR)
            except OSError as exc:
                if exc.errno not in (errno.ENOTCONN, errno.EPIPE):
                    raise
            stream_write_closed = True

        if stdin_eof and stream_eof and not to_stream and not to_stdout:
            return

        readers: list[int | socket.socket] = []
        writers: list[int | socket.socket] = []
        if not stdin_eof and len(to_stream) < MAX_BUFFER_BYTES:
            readers.append(0)
        if not stream_eof and len(to_stdout) < MAX_BUFFER_BYTES:
            readers.append(stream)
        if to_stream and not stream_write_closed:
            writers.append(stream)
        if to_stdout:
            writers.append(1)

        if not readers and not writers:
            raise Refusal("relay reached an impossible idle state")

        readable, writable, _ = select.select(readers, writers, [])

        if 0 in readable:
            block = os.read(0, min(65536, MAX_BUFFER_BYTES - len(to_stream)))
            if block:
                to_stream.extend(block)
            else:
                stdin_eof = True

        if stream in readable:
            block = stream.recv(min(65536, MAX_BUFFER_BYTES - len(to_stdout)))
            if block:
                to_stdout.extend(block)
            else:
                stream_eof = True

        if stream in writable and to_stream:
            sent = stream.send(to_stream)
            if sent <= 0:
                raise Refusal("socket write made no progress")
            del to_stream[:sent]

        if 1 in writable and to_stdout:
            sent = os.write(1, to_stdout)
            if sent <= 0:
                raise Refusal("stdout write made no progress")
            del to_stdout[:sent]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("fdpass", "stdio", "fdpass-wrong"), required=True
    )
    parser.add_argument("--binding", type=Path, required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    try:
        binding = read_binding(args.binding)
        path = validate(binding, args.port)
        stream = connect_mux(path, args.port)
        try:
            if args.mode.startswith("fdpass"):
                fdpass(stream, args.mode == "fdpass-wrong")
            else:
                relay(stream)
        finally:
            stream.close()
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError, Refusal) as exc:
        print(f"vsock connector refused: {exc}", file=sys.stderr)
        return 70


if __name__ == "__main__":
    raise SystemExit(main())
