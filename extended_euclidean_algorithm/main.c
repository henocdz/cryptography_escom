#include <stdio.h>
#include <stdlib.h>

typedef struct _gxy{
	int b,x,y;
}gxy;

gxy egcd(a,b){
	int prevr,r,prevs,s,prevt,t;
	prevr = a; // R - 1
	r = b; // Ri
	prevs = 1; // S - 1
	s = 0; // Si
	prevt = 0; // T - 1
	t = 1; // Ti

	int q, rr, sf, tf, ax;

	while(r != 0){

		q = prevr / r;
		rr = prevr % r;
		sf = prevs - (q*s);
		tf = prevt - (q*t);

		prevr = r;
		prevs = s;
		prevt = t;
		r = rr;
		s = sf;
		t = tf;
	}

	gxy res;
	res.b = a*prevs + b*prevt;
	res.x = prevs;
	res.y = prevt;
	return res;
}

int modinverse(a, z){
	gxy result = egcd(a, z);
	if (result.b == 0) return -1;
	else return result.x < 0?(z + result.x):(result.x%z); 
}

int main(void){
	int a, n;
	int res;
	printf("Set a: ");
	scanf("%d", &a);

	printf("Set n: ");
	scanf("%d", &n);
	res = modinverse(a,n);
	printf("a^(-1) mod n = %d \n", res);
}