#include <stdio.h>
#include <string.h>
char toBits(char *arr, unsigned char v) {
  int i, k=0; // for C89 compatability
  for(i = 7; i >= 0; i--){
  	arr[k] = ('0' + ((v >> i) & 1));
  	k++;
  }
  arr[8] = '\0';
}

int fromBinary(char *s) {
  return (int) strtol(s, NULL, 2);
}

void encrypt(){
	char input, aux, backup;
	unsigned char binput;
	char bits[9],bickup[8];
	printf("Introduce un caracter: ");
	scanf("%c", &input);
	binput = (int)input;
	toBits(bits, binput);
	printf("(!encrypted) %s = ascii: %c | int: %d | hex: 0x%x \n", bits, binput, binput, binput);
	/* 1) Obtener digito a mover
	 * 2) Backup de caracter a remover
	 * 3) Poner digito en su lugar
	 * ... repetir
	*/
	int k;
	for(k=0; k <= 7; k++)
		bickup[k] = bits[k];
	
	bits[1] = bickup[2];
	bits[2] = bickup[4];
	bits[3] = bickup[7];
	bits[4] = bickup[1];
	bits[5] = bickup[3];
	bits[6] = bickup[5];
	bits[7] = bickup[6];

	char biits[9];
	strcpy(biits, bits);
	int t = fromBinary(biits);
	printf(" (encrypted) %s = ascii: %c | int:%d | hex: 0x%x\n",bits, t, t, t);
}


int main(void){
	encrypt();
	return 0;
}

