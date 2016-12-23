#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <chrono>
#include <cstring>
using namespace std;
using namespace chrono;
using timepoint = time_point<high_resolution_clock>;
auto now = high_resolution_clock::now;

template<typename T>
void test_cin(T& t)
{
    timepoint tp = now();
    while(cin >> t);
    duration<double> span = duration_cast<duration<double>>(now() - tp);
    cout << span.count() << " seconds.";
}

void test_scanf(const char *format, void *data)
{
    timepoint tp = now();
    while(~scanf(format, data));
    duration<double> span = duration_cast<duration<double>>(now() - tp);
    cout << span.count() << " seconds.";
}

int main(int argc, char *argv[])
{
    int int_tmp;
    double double_tmp;
    string string_tmp;
    string_tmp.reserve(20);
    char chars_tmp[20];

    if(argc != 3) return 0;
    if(strcmp(argv[1], "int")==0)
    {
        if(strcmp(argv[2], "cin")==0)
        {
            ios::sync_with_stdio(false);
            test_cin(int_tmp);
        }
        else if(strcmp(argv[2], "cin_sync")==0)
        {
            ios::sync_with_stdio(true);
            test_cin(int_tmp);
        }
        else if(strcmp(argv[2], "scanf")==0)
            test_scanf("%d", &int_tmp);
    }
    else if(strcmp(argv[1], "double")==0)
    {
        if(strcmp(argv[2], "cin")==0)
        {
            ios::sync_with_stdio(false);
            test_cin(double_tmp);
        }
        else if(strcmp(argv[2], "cin_sync")==0)
        {
            ios::sync_with_stdio(true);
            test_cin(double_tmp);
        }
        else if(strcmp(argv[2], "scanf")==0)
            test_scanf("%lf", &double_tmp); 
    }
    else if(strcmp(argv[1], "string")==0)
    {
        if(strcmp(argv[2], "cin")==0)
        {
            ios::sync_with_stdio(false);
            test_cin(string_tmp);
        }
        else if(strcmp(argv[2], "cin_sync")==0)
        {
            ios::sync_with_stdio(true);
            test_cin(string_tmp);
        }
        else if(strcmp(argv[2], "scanf")==0)
            test_scanf("%s", chars_tmp);
    }
    return 0;
}