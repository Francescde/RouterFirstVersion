# RouterFirstVersion


compile ctypes
g++ -c -fPIC dijkstraListCFile2.cc -o dijkstraListCFile2.o
g++ -shared -W1,-soname,dijkstraMultimodalTotal.so -o dijkstraMultimodalTotal.so dijkstraMultimodalTotal.o
