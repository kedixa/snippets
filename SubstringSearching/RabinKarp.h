#ifndef RABIN_KARP_H
#define RABIN_KARP_H

#include "SubstringSearching.h"
class RabinKarp : public SubstringSearching
{
    using hash_type = long long;
private:
    const static hash_type mod = 999999937LL;
    const static hash_type set_size = 256;
    std::vector<size_t> _search_in(const char *s, size_t length) const;
public:
    RabinKarp() {}
    RabinKarp(const std::string &s)
    : SubstringSearching(s) {}
    RabinKarp(const char *s)
    : SubstringSearching(s) {}
    ~RabinKarp() {}
};

std::vector<size_t> RabinKarp::_search_in(const char *s, size_t length) const
{
    int pat_len = pattern.length();
    if(pat_len==0 || length<pat_len) return {};
    const unsigned char *ss = (unsigned char*)s;
    const unsigned char *p = (unsigned char*)pattern.c_str();

    std::vector<size_t> result;
    hash_type pat_hash = 0, txt_hash = 0;
    hash_type pow_hash = 1;
    for(int i = 0; i < pat_len - 1; ++i)
        pow_hash = (pow_hash * set_size) % mod;
    for(int i = 0; i < pat_len; i++)
        pat_hash = (pat_hash * set_size + p[i]) % mod,
        txt_hash = (txt_hash * set_size + ss[i]) % mod;

    for(int i = 0; i <= length - pat_len; ++i)
    {
        if(pat_hash == txt_hash)
        {
            if(_match(s+i, s+i+pat_len, pattern.c_str()))
                result.push_back(i);
        }
        if(i < length - pat_len)
            txt_hash = ((txt_hash - ss[i] * pow_hash) * set_size + ss[i+pat_len]) % mod;
        if(txt_hash < 0) txt_hash += mod;
    }
    return result;
}

#endif // RABIN_KARP_H
