import unittest
import substring_finder


class Substring_search_tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.substring_finders = [
            substring_finder.simplest_str_finder,
            substring_finder.KMP_algorithm
        ]

    def test_no_substring(self):
        test_string = 'asdfghjkl;'
        test_substring = 'asde'
        for func in self.substring_finders:
            self.assertEqual(func(test_string, test_substring), -1)

    def test_find_substring(self):
        test_string = 'asdfghjkl;'
        test_substring = 'fgh'
        for func in self.substring_finders:
            self.assertEqual(func(test_string, test_substring), (3, 6))

    def test_find_first_occurrence_of_substring(self):
        test_string = 'bbaaaaaaa;'
        test_substring = 'aa'
        for func in self.substring_finders:
            self.assertEqual(func(test_string, test_substring), (2, 4))


if __name__ == '__main__':
    unittest.main()