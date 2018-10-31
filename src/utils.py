## utility functions used in the main program


def strip(s):
    '''
    removing the leading and trailing non-alphabetic characters
    this function searches the non-alphabetic char from start and
    end of the string, once it encounters the first alphabetic char
    it stops stripping.
    
    input s: str
    
    >>> strip('123abc!#')
    'abc'
    >>> strip('2a3##b5c@')
    'a3##b5c'
    '''
    s = str(s) if not s is str else s 
    start, end = 0, len(s)-1
    while start < len(s)-1 and not s[start].isalpha():
        start +=1 
    while end > 0 and not s[end].isalpha():
        end -= 1
    return s[start:end+1]