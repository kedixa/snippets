#include <iostream>
#include <iomanip>
#include <cstdio>
#include <chrono>
using namespace std;
using namespace chrono;
using timepoint = time_point<high_resolution_clock>;
auto now = high_resolution_clock::now;
const int N = 10000000;

template<typename T>
void test_cout_endl(const T& t)
{
    timepoint tp = now();
    for(int i = 0; i < N; ++i)
        cout << t << endl;
    auto span = duration_cast<duration<double>>(now() - tp);
    cerr << setw(12) << span.count();
}

template<typename T>
void test_cout(const T& t)
{
    timepoint tp = now();
    for(int i = 0; i < N; ++i)
        cout << t << '\n';
    auto span = duration_cast<duration<double>>(now() - tp);
    cerr << setw(12) << span.count();
}

template<typename T>
void test_printf(const char *format, const T& t)
{
    timepoint tp = now();
    for(int i = 0; i < N; ++i)
        printf(format, t);
    auto span = duration_cast<duration<double>>(now() - tp);
    cerr << setw(12) << span.count();
}

int main()
{
    ios::sync_with_stdio(false);
    int int_tmp = 123456789;
    double double_tmp = 12345.6789;
    const char *chars_tmp = "123456789";
    cerr << "          "
         << "   cout_endl"
         << "        cout"
         << "      printf\n";
    cerr << "int       ";
    test_cout_endl(int_tmp);
    test_cout(int_tmp);
    test_printf("%d\n", int_tmp);
    cerr << endl;

    cerr << "double    ";
    test_cout_endl(double_tmp);
    test_cout(double_tmp);
    test_printf("%lf\n", double_tmp);
    cerr << endl;

    cerr << "string    ";
    test_cout_endl(chars_tmp);
    test_cout(chars_tmp);
    test_printf("%s\n", chars_tmp);
    cerr << endl;
    return 0;
}