main:main.c ./src/serial.c 
	gcc ./src/serial.c main.c -o xbox
build:./src/tool.cpp
	g++ -fpic -shared -o tool.so ./src/tool.cpp
clean:
	rm -fr  xbox
	
