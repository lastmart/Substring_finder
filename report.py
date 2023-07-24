from timeit import default_timer
import re
import os


class Reporter:
    def __init__(self, functions: list):
        for e in functions:
            if not hasattr(e, "__call__"):
                raise TypeError(f"{e} is not a function")
        self.substring_finders = functions
        self.all_statistics = []

    def make_stats(self):
        stats = self.get_stats()
        finders_docs = [
            self.parse_documentation(e)
            for e in map(lambda x: x.__doc__, self.substring_finders)
        ]
        report_data = [e for e in zip(*[e for e in finders_docs])]
        report = [
            f'|Parameter name|{"|".join(report_data[0])}|',
            "|-" * (len(self.substring_finders) + 1) + "|",
            f'|Time complexity|{"|".join(report_data[1])}|',
            f'|Memory complexity|{"|".join(report_data[2])}|',
        ]
        stats_lines = [f"|{'|'.join(e)}|" for e in stats]
        for e in stats_lines:
            report.append(e)
        with open("report.md", "w") as f:
            f.write("\n".join(report))

    def get_stats(self):
        texts_path = os.path.dirname(__file__) + "\\texts\\"
        comparing_parameters = [
            (
                r"BigDataWithoutRepeating.txt",
                "них",
                "Big data without repeating (len(substring) == 3)",
                50,
            ),
            (
                r"BigDataWithoutRepeating.txt",
                "Mon Dieu",
                "Big data without repeating (len(substring) == 8)",
                50,
            ),
            (
                r"BigDataWithoutRepeating.txt",
                "Доктор посмотрел",
                "Big data without repeating (len(substring) == 16)",
                50,
            ),
            (
                r"BigDataWithoutRepeating.txt",
                "Зала ресторации превратилась",
                "Big data without repeating (len(substring) == 28)",
                50,
            ),
            (
                r"BeginningAndEndingOfSubstringRepeatManyTimes.txt",
                "the same part finish the same part",
                "Beginning and ending of substring repeat many times",
                50,
            ),
            (
                r"BeginningOfSubstringRepeatManyTimes.txt",
                "Hello my dear Sun",
                "Beginning of substring repeat many times",
                50,
            ),
            (
                r"SubstringContainsFewDifferentLetters.txt",
                "aaaaaaaaff",
                "Substring contains few different letters",
                50,
            ),
        ]
        for parameter in comparing_parameters:
            with open(texts_path + parameter[0], encoding="utf-8") as f:
                test_text = f.read()
                self.all_statistics.append(
                    self._get_base_statistics(test_text, *parameter[1:])
                )
                del test_text
        return self.all_statistics

    @staticmethod
    def parse_documentation(doc: str) -> list:
        name = re.search("(?<=Name:).+", doc)[0].strip()
        time_complexity = re.search("(?<=Time complexity:).+", doc)[0].strip()
        memory_complexity = re.search("(?<=Memory complexity:).+", doc)[0].strip()
        return [name, time_complexity, memory_complexity]

    def _get_base_statistics(
        self, test_text: str, test_substring: str, statistic_name: str, repeats: int
    ):
        statistics = [statistic_name]
        for finder in self.substring_finders:
            finder(test_text, test_substring)
            start_time = default_timer()
            for _ in range(repeats):
                finder(test_text, test_substring)
            statistics.append(str((default_timer() - start_time) / repeats))
        return statistics
