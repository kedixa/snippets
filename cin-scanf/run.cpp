#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
using namespace std;

int main(int argc, char *argv[])
{
    if(argc != 2) return 0;
    string cmd;

    for(auto type1 : {"    int", " double", " string"})
        for(auto type2 : {" cin_sync", " cin     ", " scanf   "})
        {
            cmd = string(argv[1]) + type1 + type2 + " <" + type1 + ".dat ";
            cout << cmd << ": ";
            cout.flush();
            system(cmd.c_str());
            cout << endl;
        }
    return 0;
}