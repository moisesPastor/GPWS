all: escalaIndex
INCLUDE=-I. -I./LIB/
OPEN_LIBS=`pkg-config --cflags --libs opencv4` -lpugixml


PROG_LIBS=./LIB/libXmlPAGE.o ./LIB/libPoints.o


escalaIndex:  escalaIndex.cc 
	make -C LIB/
	g++ -o escalaIndex escalaIndex.cc   ${PROG_LIBS} ${INCLUDE}  ${OPEN_LIBS}  -O3  

clean:
	rm -f escalaIndex *.o


