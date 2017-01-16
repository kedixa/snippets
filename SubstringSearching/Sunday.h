#ifndef SUNDAY_H
#define SUNDAY_H

#include "SubstringSearching.h"
class Sunday : public SubstringSearching
{
private:
    std::vector<size_t> _search_in(const char *s, size_t length) const;
    void init_next();
    std::vector<int> next;
public:
    Sunday() {}
    Sunday(const std::string &s)
    : SubstringSearching(s) {
        init_next();
    }
    Sunday(const char *s)
    : SubstringSearching(s) {
        init_next();
    }
    ~Sunday() {}
};

void Sunday::init_next()
{
    int pat_len = pattern.length();
    const unsigned char *p = (unsigned char*)pattern.c_str();
    next.resize(256, pat_len + 1);
    for(int i = 0; i < pat_len; ++i)
        next[p[i]] = pat_len - i;
}

std::vector<size_t> Sunday::_search_in(const char *s, size_t length) const
{
    int pat_len = pattern.length();
    const unsigned char *ss = (unsigned char*)s; // must be unsigned char
    const unsigned char *p = (unsigned char*)pattern.c_str();
    if(pat_len==0 || length < pat_len) return {}; // make no sense

    std::vector<size_t> result;
    for(int i = 0; i <= length - pat_len;)
    {
        if(_match(s+i, s+i+pat_len, pattern.c_str()))
            result.push_back(i++);
        else i += next[ss[i + pat_len]];
    }
    return result;
}

#endif // SUNDAY_H
