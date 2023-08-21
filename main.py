from report import Reporter
import substring_finder
import os


if __name__ == '__main__':
    substring_finders = [
        substring_finder.brute_force,
        substring_finder.KMP_algorithm,
        substring_finder.z_function_finder,
        substring_finder.BMH_algorithm,
        substring_finder.AC_algorithm,
    ]
    comparing_parameters = [
        (
            r"BigDataWithoutRepeating.txt",
            "ними",
            "Big data without repeating (len(substring) == 4)",
        ),
        (
            r"BigDataWithoutRepeating.txt",
            "Сонский",
            "Big data without repeating (len(substring) == 7)",
        ),
        (
            r"BigDataWithoutRepeating.txt",
            "Мы предлагаем вам",
            "Big data without repeating (len(substring) == 17)",
        ),
        (
            r"BigDataWithoutRepeating.txt",
            "%D0%9A%D0%BE%D0%BB%D1%8C%D1%86%D0%B0",
            "Big data without repeating (len(substring) == 36)",
        ),
        (
            r"SmallDataWithoutRepeating.txt",
            "них",
            "Small data without repeating (len(substring) == 3)",
        ),
        (
            r"SmallDataWithoutRepeating.txt",
            "Mon Dieu",
            "Small data without repeating (len(substring) == 8)",
        ),
        (
            r"SmallDataWithoutRepeating.txt",
            "Доктор посмотрел",
            "Small data without repeating (len(substring) == 16)",
        ),
        (
            r"SmallDataWithoutRepeating.txt",
            "Зала ресторации превратилась",
            "Small data without repeating (len(substring) == 28)",
        ),
        (
            r"BeginningAndEndingOfSubstringRepeatManyTimes.txt",
            "the same part finish the same part",
            "Beginning and ending of substring repeat many times",
        ),
        (
            r"BeginningOfSubstringRepeatManyTimes.txt",
            "Hello my dear Sun",
            "Beginning of substring repeat many times",
        ),
        (
            r"SubstringContainsFewDifferentLetters.txt",
            "aaaaaaaaff",
            "Substring contains few different letters",
        ),
    ]
    texts_path = os.path.dirname(__file__) + "\\texts\\"
    comparing_parameters = list(map(lambda x: (texts_path + x[0], x[1], x[2]),
                                    comparing_parameters))
    reporter = Reporter(substring_finders, comparing_parameters, 51)
    reporter.generate_statistics()
