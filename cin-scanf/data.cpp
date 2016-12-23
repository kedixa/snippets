#include <iostream>
#include <fstream>
#include <cstdio>
using namespace std;

const int N = 10000000;
const double pi = 3.14159265358979;
int main()
{
    ofstream ofs;
    ofs.open("int.dat");
    for(int i = 0; i < N; ++i)
        ofs << i + N << '\n';
    ofs.close();

    ofs.open("double.dat");
    for(int i = 0; i < N; ++i)
        ofs << (i+1) * pi << '\n';
    ofs.close();

    ofs.open("string.dat");
    char c[] = "abcdefgh";
    for(int i = 0; i < N; ++i)
        ofs << c << '\n';
    ofs.close();
    return 0;
}