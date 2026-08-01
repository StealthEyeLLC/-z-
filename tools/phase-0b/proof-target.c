#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
static void hex(FILE *f,const unsigned char *p,size_t n){for(size_t i=0;i<n;i++)fprintf(f,"%02x",p[i]);}
int main(int argc,char **argv){
  char cwd[PATH_MAX]; if(!getcwd(cwd,sizeof(cwd))) return 125;
  const char *env=getenv("Z_PHASE0B_ENV");
  printf("argc=%d\n",argc); for(int i=0;i<argc;i++){printf("argv%d_len=%zu\nargv%d_hex=",i,strlen(argv[i]),i);hex(stdout,(unsigned char*)argv[i],strlen(argv[i]));putchar('\n');}
  printf("cwd_len=%zu\ncwd_hex=",strlen(cwd));hex(stdout,(unsigned char*)cwd,strlen(cwd));putchar('\n');
  if(env){printf("env_present=1\nenv_len=%zu\nenv_hex=",strlen(env));hex(stdout,(unsigned char*)env,strlen(env));putchar('\n');}else puts("env_present=0");
  fflush(stdout);
  const unsigned char errbytes[]={0x5a,0x00,0x45,0xff,0x0a}; fwrite(errbytes,1,sizeof(errbytes),stderr);fflush(stderr);
  unsigned char buf[8192]; ssize_t n; while((n=read(STDIN_FILENO,buf,sizeof(buf)))>0){if(write(STDOUT_FILENO,buf,(size_t)n)!=n)return 124;} if(n<0)return 123;
  const char *mode=getenv("Z_PHASE0B_MODE");
  if(mode && strncmp(mode,"exit:",5)==0) return atoi(mode+5);
  if(mode && strncmp(mode,"signal:",7)==0){raise(atoi(mode+7));return 122;}
  if(mode && strncmp(mode,"sleep_ms:",9)==0){long ms=atol(mode+9);struct timespec ts={ms/1000,(ms%1000)*1000000};nanosleep(&ts,NULL);}
  return 0;
}
