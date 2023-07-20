from trie import Trie, Node
from queue import Queue
from typing import Union


def simplest_str_finder(haystack: str, needle: str) -> Union[tuple, int]:
    """
    Name: The simplest search for a substring in a string
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
    Name: Knuth-Morris-Pratt algorithm
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
    Name: Algorithm using z function
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
    Name: Boyer-Moore-Horspool algorithm
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


def AC_algorithm(haystack: str, needles: Union[list, str]) -> Union[tuple, int]:
    """
    Name: Aho-Corasick algorithm
    Explanation: https://www.youtube.com/watch?v=-KCd8UUwU38
    Time complexity: O(len(needles) + len(haystack))
    Memory complexity: O(len(needles))
    This version of the algorithm finds the first occurrence of one
    of the needles in the haystack
    """
    trie = Trie(needles)
    build_suffix_links(trie)
    find_extra_terminal_nodes(trie)
    alphabet = set(''.join(needles))
    state = trie.root
    counter = 0
    for e in haystack:
        counter += 1
        child = state.children.get(e)
        state = state.suffix if child is None else child
        if e not in alphabet or state is None:
            state = trie.root
            continue
        if state.is_terminal:
            return counter - get_depth_of_node(trie, state), counter
    return -1


def build_suffix_links(trie: Trie):
    queue = Queue()
    queue.put((trie.root, trie.root, None, None))
    while not queue.empty():
        e = queue.get()
        current_element = e[0]
        current_element.find_suffix(*e[1:])
        if len(current_element.children) <= 0:
            continue
        for e in [(value, trie.root, current_element, key) for key, value in
                  current_element.children.items()]:
            queue.put(e)


def find_extra_terminal_nodes(trie: Trie):
    queue = Queue()
    queue.put(trie.root)
    while not queue.empty():
        current = node = queue.get()
        while not current.is_terminal and node.suffix:
            current.is_terminal = node.suffix.is_terminal
            node = node.suffix
        for e in current.children.values():
            queue.put(e)


def get_depth_of_node(trie: Trie, node: Node):
    queue = Queue()
    queue.put((trie.root, 0))
    while not queue.empty():
        n, depth = queue.get()
        if n is node:
            return depth
        for e in n.children.values():
            queue.put((e, depth + 1))
    return -1
