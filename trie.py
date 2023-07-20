class Trie:
    def __init__(self, words: list = None):
        self._root = Node()
        if words is not None:
            self.add(words)

    def add(self, words):
        if isinstance(words, str):
            self._add_word(words)
        elif hasattr(words, '__iter__'):
            for word in words:
                self._add_word(word)
        else:
            raise TypeError(f"Trie can't contains {type(words)}")

    def _add_word(self, word: str):
        current_node = self._root
        for char in word:
            child = current_node.children.get(char)
            if child is None:
                current_node.children[char] = Node()
                current_node = current_node.children[char]
            else:
                current_node = child
        current_node.is_terminal = True

    @property
    def root(self):
        return self._root


class Node:
    def __init__(self):
        self.is_terminal = False
        self.children = {}
        self.suffix = None

    def find_suffix(self, root, parent, char):
        if self is root:
            return
        v = parent.suffix
        while v is not None:
            child = v.children.get(char)
            if child is not None:
                self.suffix = child
                return
            v = v.suffix
        self.suffix = root
