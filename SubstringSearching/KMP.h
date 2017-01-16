#ifndef KMP_H
#define KMP_H 

#include "SubstringSearching.h"
class KMP : public SubstringSearching
{
private:
    std::vector<size_t> _search_in(const char *s, size_t length) const;
    std::vector<int> prefix;
    void init_prefix();
public:
    KMP() {}
    KMP(const std::string &s)
    : SubstringSearching(s) {
        init_prefix();
    }
    KMP(const char *s)
    : SubstringSearching(s) {
        init_prefix();
    }
    ~KMP() {}
};

void KMP::init_prefix()
{
    int pat_len = pattern.length();
    if(pat_len == 0) return;
    prefix.resize(pat_len);
    prefix[0] = -1;
    int k = -1, i = 0;
    while(i < pat_len - 1)
    {
        if(k==-1 || pattern[i]==pattern[k])
        {
            ++i, ++k;
            if(pattern[i] != pattern[k]) prefix[i] = k;
            else prefix[i] = prefix[k];
        }
        else k = prefix[k];
    }
}

std::vector<size_t> KMP::_search_in(const char *s, size_t length) const
{
    int pat_len = pattern.length();
    if(pat_len==0 || length < pat_len) return {};

    std::vector<size_t> result;
    int i = 0, j = 0;
    while(i < length)
    {
        if(j==-1 || s[i]==pattern[j])
        {
            ++i, ++j;
            if(j == pat_len)
            {
                result.push_back(i - j);
                i = i - j + 1;
                j = 0;
            }
        }
        else j = prefix[j];
    }
    return result;
}

#endif // KMP_H
