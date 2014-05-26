#include <stdio.h>
#include <stdlib.h>
#define ASC 65

int cypher(char khar, int a, int b){
	int ihar,r ;
	ihar = (int)khar - ASC;
	if(ihar < 0) // ASCII no valido
		exit(1);
	r = (a * ihar) +  b;
	while(r > 26)
		r = r % 26;
	return r + ASC;
}

int gcd(int a,int b){
	if(b==0)
		return a;
	else
		return gcd(b,a%b);
}

int main(void){
	char khar;
	int a,b, pos;

	printf("Indica alpha: ");
	scanf("%d", &a);
	printf("Indica beta: ");
	scanf("%d", &b);

	while(gcd(a,b) != 1){
		system("clear");
		printf("Los numeros %d y %d  no son COPRIMOS.\n", a, b);
		printf("Indica alpha: ");
		scanf("%d", &a);
		printf("Indica beta: ");
		scanf("%d", &b);
	}

	FILE *input, *output;
	input = fopen("message.cyp", "r");
	output = fopen("omessage.cyp", "w");
	while( (khar = fgetc(input)) != EOF ){
		if( khar == '\0' || khar == '\r' )
			continue;
		if(khar == ' '){
			fputc( (int)'~', output);
			continue;
		}
		pos = cypher(khar, a, b);
		fputc(pos, output);
	}

	fclose(input);
	fclose(output);

	system("vi omessage.cyp");
	return 0;
}
