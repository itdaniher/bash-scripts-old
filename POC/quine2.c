#include <stdio.h>
int main() {
  char *foo = "#include <stdio.h>\nint main() {\n  char *foo = \"@@\";\n  int i,j;\n  for(i=0;foo[i];i++) {\n    if(foo[i]==foo[i+1] && foo[i]=='@') {\n      for(j=0;foo[j];j++) {\n        if(foo[j]=='\\n') { putchar('\\\\'); putchar('n'); } \n        else if(foo[j]=='\\\\') { putchar('\\\\'); putchar('\\\\'); }\n        else if(foo[j]=='\"') { putchar('\\\\'); putchar('\"'); }\n        else putchar(foo[j]);\n      }\n      i++; \n    }\n    else putchar(foo[i]);\n  }\n  putchar('\\n');\n  return 0;\n}";
  int i,j;
  for(i=0;foo[i];i++) {
    if(foo[i]==foo[i+1] && foo[i]=='@') {
      for(j=0;foo[j];j++) {
        if(foo[j]=='\n') { putchar('\\'); putchar('n'); } 
        else if(foo[j]=='\\') { putchar('\\'); putchar('\\'); }
        else if(foo[j]=='"') { putchar('\\'); putchar('"'); }
        else putchar(foo[j]);
      }
      i++; 
    }
    else putchar(foo[i]);
  }
  putchar('\n');
  return 0;
}

