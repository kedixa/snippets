#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <chrono>
#include <cassert>
#include <iomanip>
#include "BruteForce.h"
#include "KMP.h"
#include "RabinKarp.h"
#include "Sunday.h"
using namespace std;
using namespace chrono;

string dna, shakespeare, novel;
static int COUNT = 200;
auto now = high_resolution_clock::now;

string read_data(string filename)
{
    ifstream f("../data/" + filename, ifstream::binary);
    string data((istreambuf_iterator<char>(f)), istreambuf_iterator<char>());
    f.close();
    if(filename=="dna.txt")
        data.erase(remove(data.begin(), data.end(), '\n'), data.end());
    return data;
}

void test_one(SubstringSearching *ss, string &data)
{
    auto start = now();
    for(int i = 0; i < COUNT; ++i)
        ss->search_in(data);
    auto span = duration_cast<duration<double>>(now() - start);
    cout << setw(12) << span.count();
}

void test(string p, string &data)
{
    BruteForce bf(p);
    KMP kmp(p);
    RabinKarp rk(p);
    Sunday sd(p);
    test_one(&bf, data);
    test_one(&kmp, data);
    test_one(&rk, data);
    test_one(&sd, data);
}

void check(string p, string &data)
{
    BruteForce bf(p);
    KMP kmp(p);
    RabinKarp rk(p);
    Sunday sd(p);
    auto v = bf.search_in(data);
    assert(v == kmp.search_in(data));
    assert(v == rk.search_in(data));
    assert(v == sd.search_in(data));
}

int main()
{
    dna = read_data("dna.txt");
    shakespeare = read_data("shakespeare.txt");
    novel = read_data("novel.txt");
    check("AGCTAGCT", dna);

    cout << setw(12) << "dataset" << setw(12) << "BruteForce" << setw(12)
        << "KMP" << setw(12) << "RabinKarp" << setw(12) << "Sunday\n";
    cout << setw(12) << "dna";
    test("CAATCT", dna);
    cout << endl;
    cout << setw(12) << "shakespeare";
    test("himself", shakespeare);
    cout << endl;
    cout << setw(12) << "novel";
    test("小秋说", novel);
    cout << endl;

    return 0;
}