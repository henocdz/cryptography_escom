#ifndef EGCD_H_INCLUDED
#define EGCD_H_INCLUDED

typedef struct _gxy{
	int b,x,y;
}gxy;

gxy egcd(int a, int b);
int modinverse(int a,int z);

#endif