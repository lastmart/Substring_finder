from timeit import default_timer
from math import sqrt
from typing import Union
import re
import os


class Reporter:
    _comparing_parameters = [
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
    _alpha_dict = {6: 2.5706,
                   11: 2.2281,
                   16: 2.1314,
                   21: 2.0860,
                   26: 2.0555,
                   31: 2.0423,
                   36: 2.0301,
                   41: 2.0211,
                   51: 2.0086,
                   101: 1.9840}

    def __init__(self, functions: list, repeats: int):
        for e in functions:
            if not hasattr(e, "__call__"):
                raise TypeError(f"{e} is not a function")
        if repeats not in self._alpha_dict:
            raise ValueError(
                f'You can only set the following repeat values\n'
                f'{", ".join([str(x) for x in self._alpha_dict.keys()])}')
        self.alpha = self._alpha_dict[repeats]
        self.repeats = repeats
        self.substring_finders = functions
        self.all_statistics = None

    def generate_statistics(self):
        self.all_statistics = self.get_stats()
        self._generate_report_in_md_format()
        self._calculate_confidence_interval_for_each_result()

    def _generate_report_in_md_format(self):
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
        stats_lines = [f"|{'|'.join(e)}|" for e in self.all_statistics]
        report.extend(stats_lines)
        with open("report.md", "w") as f:
            f.write("\n".join(report))

    def get_stats(self):
        texts_path = os.path.dirname(__file__) + "\\texts\\"
        stats = []
        for parameter in self._comparing_parameters:
            with open(texts_path + parameter[0], encoding="utf-8") as f:
                test_text = f.read()
                stats.append(
                    self._get_base_statistics(test_text, *parameter[1:],
                                              repeats=self.repeats)
                )
                del test_text
        return stats

    @staticmethod
    def parse_documentation(doc: str) -> list:
        name = re.search("(?<=Name:).+", doc)[0].strip()
        time_complexity = re.search("(?<=Time complexity:).+", doc)[0].strip()
        memory_complexity = re.search("(?<=Memory complexity:).+", doc)[
            0].strip()
        return [name, time_complexity, memory_complexity]

    def _get_base_statistics(
            self, test_text: str, test_substring: str, statistic_name: str,
            repeats: int
    ) -> list[str]:
        Reporter._save_intermediate_results(statistic_name)
        statistics = [statistic_name]
        for finder in self.substring_finders:
            finder(test_text, test_substring)
            finder(test_text, test_substring)
            time_of_work = []
            for _ in range(repeats):
                start_time = default_timer()
                finder(test_text, test_substring)
                end_time = default_timer()
                time_of_work.append(end_time - start_time)
            statistics.append(f'{(sum(time_of_work) / repeats):0.6f}')
            Reporter._save_intermediate_results(
                [finder.__name__] + time_of_work)
        return statistics

    @staticmethod
    def _save_intermediate_results(data: Union[list, str]) -> None:
        with open(r'intermediate_results.txt', encoding='utf-8',
                  mode='a') as f:
            f.writelines(f'{data}\n')

    def _calculate_confidence_interval_for_each_result(self):
        float_pattern = re.compile(r'\d+\.\d+')
        confidence_interval_list = []
        function_name_pattern = re.compile("|".join(
            map(lambda x: x.__name__, self.substring_finders)))
        with open('intermediate_results.txt', mode='r+',
                  encoding='utf-8') as f:
            data = f.readlines()
            for calculation in data:
                if re.search(function_name_pattern, calculation) is None:
                    confidence_interval_list.append('')
                    continue
                time_list = [float(x) for x in
                             re.findall(float_pattern, calculation)]
                confidence_interval = self._calculate_confidence_interval(
                    time_list)
                confidence_interval_list.append(
                    f' confidence interval: {confidence_interval}')

    def _calculate_confidence_interval(self, time_list: list) -> float:
        average_time = sum(time_list) / self.repeats
        standard_deviation = sqrt((1 / (self.repeats - 1)) * (
            sum([(t - average_time) ** 2 for t in time_list])))
        return (self._alpha_dict[self.repeats] * standard_deviation /
                sqrt(self.repeats))
