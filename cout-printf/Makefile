all: test.out
	./test.out > /dev/null

test.out: test.cpp
	g++ -std=c++11 test.cpp -o test.out

clean:
	rm test.out