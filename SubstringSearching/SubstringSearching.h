#ifndef SUBSTRING_SEARCHING_H
#define SUBSTRING_SEARCHING_H

#include <string>
#include <vector>
class SubstringSearching
{
protected:
    std::string pattern;
    virtual std::vector<size_t> _search_in(const char*, size_t) const = 0;
    bool _match(const char *first, const char *last, const char *first2)const
    {
        while(first != last && *first == *first2) ++first, ++first2;
        return first == last;
    }
public:
    SubstringSearching(){}
    SubstringSearching(const std::string &s)
    { pattern = s; }
    SubstringSearching(const char *s)
    { pattern = std::string(s); }

    std::vector<size_t> search_in(const std::string &s) const
    { return _search_in(s.c_str(), s.length()); }
    std::vector<size_t> search_in(const char* s, size_t length)
    { return _search_in(s, length); }
    
    virtual ~SubstringSearching() {}
};

#endif // SUBSTRING_SEARCHING_H
