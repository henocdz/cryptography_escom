#include <stdio.h>
#include <stdlib.h>



int main(void){
	int r,g,b, image[666816][3];
	char i[255];
	FILE *input;

	printf("Introduce la ruta de la imagen: ");
	scanf("%s", i);

	printf("Introduce R: ");
	scanf("%d", r);
	printf("Introduce G: ");
	scanf("%d", g);
	printf("Introduce B: ");
	scanf("%d", b);

	input = fopen(i, "r");
	int byte, k=0;
	for(k; k < 54; k++) byte = getc(input);

	k = 0;
	for(k; k<666816;k++){
		image[k][0] = getc(input);
		image[k][1] = getc(input);
		image[k][2] = getc(input);

		printf("pixel: %d (%d,%d,%d)\n", image[k][0],image[k][1],image[k][2]);

	}

	return 0;
}