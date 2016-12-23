#include <iostream>
#include <sstream>
#include <cstdio>
#include <chrono>
#include <string>
#include <iomanip>
using namespace std;
using namespace chrono;
using timepoint = time_point<high_resolution_clock>;
auto now = high_resolution_clock::now;
const int N = 10000000;

template<typename T>
void test_in(const string &text, const char *format)
{
    T tmp;
    istringstream iss;
    timepoint tp = now();
    for(int i = 0; i < N; ++i)
    {
        iss.str(text);
        iss >> tmp;
    }
    auto span = duration_cast<duration<double>>(now() - tp);
    cout << setw(12) << span.count();

    tp = now();
    for(int i = 0; i < N; ++i)
        sscanf(text.c_str(), format, &tmp);
    span = duration_cast<duration<double>>(now() - tp);
    cout << setw(12) << span.count();
}

template<typename T>
void test_out(const char *format, const T &t)
{
    char buf[50];
    ostringstream oss;
    timepoint tp = now();
    for(int i = 0; i < N; ++i)
        oss << t;
    auto span = duration_cast<duration<double>>(now() - tp);
    cout << setw(12) << span.count();

    tp = now();
    for(int i = 0; i < N; ++i)
        sprintf(buf, format, &t);
    span = duration_cast<duration<double>>(now() - tp);
    cout << setw(12) << span.count();
}

int main()
{
    int int_tmp = 123456789;
    double double_tmp = 1234.56789;

    cout << "istringstream     sscanf\n";
    test_in<int>("123456789", "%d");
    cout << endl;
    test_in<double>("1234.56789", "%lf");
    cout << endl << endl;

    cout << "ostringstream    sprintf\n";
    test_out<int>("%d", int_tmp);
    cout << endl;
    test_out<double>("%lf", double_tmp);
    cout << endl;
    return 0;
}
