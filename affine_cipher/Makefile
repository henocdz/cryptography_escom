affine: main.o egcd.o
	gcc -o  out egcd.o main.o

main.o: main.c
	gcc -c main.c
egcd.o: egcd.h egcd.c
	gcc -c egcd.c

run: affine
	./out

clean:
	rm main.o
	rm egcd.o
	rm out
