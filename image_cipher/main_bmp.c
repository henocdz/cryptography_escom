#include <stdio.h>
#include <stdlib.h>
#include "libbmp/bmpfile.c"



int main(void){
	int r,g,b, image[66528][3];
	char i[255];
	FILE *input;

	printf("Introduce la ruta de la imagen: ");
	scanf("%s", i);

	printf("Introduce R: ");
	scanf("%d", &r);
	printf("Introduce G: ");
	scanf("%d", &g);
	printf("Introduce B: ");
	scanf("%d", &b);

	input = fopen(i, "r");
	FILE *output;
	bmpfile_t *bmp;
	
	if( (bmp = bmp_create(264,252,0)) == NULL ){
		printf("-----\n");
		return 1;
		
	}

	output = fopen("o.bmp","w");
	int byte, k=0;
	for(k; k < 54; k++) byte = getc(input);

	k = 0;
	int ri,gi,bi;
	for(k; k<666816;k++){
		image[k][0] = getc(input);
		image[k][1] = getc(input);
		image[k][2] = getc(input);
		ri = image[k][0] + r;
		gi = image[k][1] + g;
		bi = image[k][2] + b;

		while(ri > 255){
			ri = ri%256;
		}
		while(gi > 255){
			gi = gi%256;
		}

		while(bi > 255){
			bi = bi%256;
		}

		
		printf("pixel: %d (%d,%d,%d) | [%d,%d,%d]\n",k, image[k][0],image[k][1],image[k][2], ri,gi,bi);

	}

	fclose(input);
	fclose(output);

	return 0;
}