#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Anastasiya Kostyanitsyna

import doctest


def paligram(line):
    """
       This is function shows if the word is a paligram.
    >>> paligram('mama')
    False
    >>> paligram('ama')
    True
    >>> paligram(23)
    Traceback (most recent call last):
        ...
    ValueError: Argument line must be str
    >>> paligram('')
    Traceback (most recent call last):
        ...
    ValueError: Argument line is not a word
    """
    if not isinstance(line, str):
        raise ValueError('Argument n must be str')
    elif len(line) == 0:
        raise ValueError('Argument n is not a word')
    else:
        line = line.strip(' ,./<>"][{}+=-_)(*&^%$#@!~?|\;:')
        line = line.lower()
        pal = line[::-1]
        if pal == line:
            print(True)
        else:
            print(False)
    return


if __name__ == "__main__":
    doctest.testmod()

