#ifndef BRUTE_FORCE_H
#define BRUTE_FORCE_H

#include "SubstringSearching.h"
class BruteForce : public SubstringSearching
{
private:
    std::vector<size_t> _search_in(const char *s, size_t length) const;
public:
    BruteForce() {}
    BruteForce(const std::string &s)
    : SubstringSearching(s) {}
    BruteForce(const char *s)
    : SubstringSearching(s) {}
    ~BruteForce() {}
};

std::vector<size_t> BruteForce::_search_in(const char *s, size_t length) const
{
    int pat_len = pattern.length();
    if(pat_len==0 || length<pat_len) return {}; // make no sense

    std::vector<size_t> result;
    for(int i = 0; i <= length - pat_len; ++i)
        if(_match(s+i, s+i+pat_len, pattern.c_str()))
            result.push_back(static_cast<size_t>(i));
    return result;
}

#endif // BRUTE_FORCE_H
