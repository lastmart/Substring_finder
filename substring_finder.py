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
    Explanation: https://www.youtube.com/watch?v=7g-WEBj3igk
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


def z_function_finder(haystack: str, needle: str, separator="$") -> Union[tuple, int]:
    """
    Explanation: https://youtu.be/BP9LXwosFco
    Time complexity: O(len(haystack) + len(needle))
    Memory complexity: O(len(haystack) + len(needle))
    """
    if len(haystack) < len(needle):
        return -1
    if len(needle) < 1:
        return 0
    z = z_function(needle + separator + haystack)
    try:
        begin = z.index(len(needle)) - len(needle) - 1
        return begin, begin + len(needle)
    except ValueError:
        return -1


def z_function(text: str) -> list:
    l, r = 0, 1
    z = [0] * len(text)
    for i in range(1, len(text)):
        z[i] = max(0, min(z[i - l], r - i))
        while i + z[i] < len(text) and text[i + z[i]] == text[z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def BMH_algorithm(haystack: str, needle: str) -> Union[tuple, int]:
    """
    Boyer-Moore-Horspool algorithm
    Explanation: https://yandex.ru/video/preview/2201665387922285863
    Time complexity: O(len(haystack) * len(needle))
    Memory complexity: O(len(needle))
    Amortization time complexity: O(len(haystack / |Σ|)
    where |Σ| is power of alphabet
    """
    if len(haystack) < len(needle):
        return -1
    if len(needle) < 1:
        return 0
    d = d_function(needle)
    border = len(needle) - 1
    k, l = 0, 1
    while border < len(haystack):
        while haystack[border - k] == needle[-l]:
            l += 1
            k += 1
            if l == len(needle):
                return border - len(needle) + 1, border + 1
        else:
            control_char = haystack[border] if k == 0 else needle[-1]
            k, l = 0, 1
            if control_char in d:
                border += d[control_char]
            else:
                border += len(needle)
    return -1


def d_function(text: str) -> dict:
    d = dict()
    pointer = 0
    for e in text[-2::-1]:
        pointer += 1
        if e in d:
            continue
        d[e] = pointer
    if text[-1] not in d:
        d[text[-1]] = len(text)
    return d
