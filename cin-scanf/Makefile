ifeq ($(OS), Windows_NT)
	prefix =
else
	prefix = ./
endif

all: data test

data: data.out
	./data.out

test: test.out run.out
	./run.out $(prefix)test.out

data.out: data.cpp
	g++ -std=c++11 data.cpp -o data.out

test.out: test.cpp
	g++ -std=c++11 test.cpp -o test.out

run.out: run.cpp
	g++ -std=c++11 run.cpp -o run.out

clean:
	rm int.dat double.dat string.dat run.out test.out data.out