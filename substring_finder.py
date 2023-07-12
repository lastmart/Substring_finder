import re
from typing import Union


def simplest_str_finder(haystack: str, needle: str) -> Union[tuple, int]:
    """
    The simplest search for a substring in a string
    Time complexity: O(len(haystack) * len(needle))
    Memory complexity: O(1)
    """
    if len(haystack) < len(needle):
        return -1
    if len(needle) < 1:
        return 0
    for i in range(len(haystack) - len(needle) + 1):
        success = True
        for j in range(len(needle)):
            if haystack[i + j] != needle[j]:
                success = False
        if success:
            return i, i + len(needle)
    return -1


def KMP_algorithm(haystack: str, needle: str) -> Union[tuple, int]:
    """
    Knuth-Morris-Pratt algorithm
    Time complexity: O(len(haystack) + len(needle))
    Memory complexity: O(len(needle))
    """
    if len(haystack) < len(needle):
        return -1
    if len(needle) < 1:
        return 0
    pi = prefix_function(needle)
    i = 0
    j = 0
    while i < len(haystack):
        if j == len(needle):
            return i - len(needle), i
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        elif j != 0:
            j = pi[j - 1]
        else:
            i += 1
    return -1


def prefix_function(text: str) -> list:
    pi = [0] * len(text)
    j = 0
    i = 1
    while i < len(text):
        if text[i] == text[j]:
            pi[i] = j + 1
            i += 1
            j += 1
        elif j == 0:
            pi[i] = 0
            i += 1
        else:
            j = pi[j - 1]
    return pi


def regex_finder(haystack, needle):
    match = re.search(haystack, needle)
    if match is None:
        return -1
    else:
        return match.span()
