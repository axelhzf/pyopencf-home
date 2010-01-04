#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	FILE *name;
	int i;
	name = fopen(argv[2],"w");
	for (i = 0; i < atoi(argv[1]); i++) {
		fprintf(name,"Hello,world!!\n");
	}
	fclose(name);
}
	
