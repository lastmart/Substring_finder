from timeit import default_timer
from typing import Union, Callable
from math import sqrt
import re


def save_intermediate_results(data: Union[list, str],
                              mode: str,
                              path_to_save: str) -> None:
    with open(path_to_save, encoding='utf-8', mode=mode) as f:
        if isinstance(data, str):
            f.write(f'{data}\n')
        elif isinstance(data, list):
            f.writelines(data)
        else:
            raise ValueError(f'Incorrect tipe to save: {type(data)}')


def calculate_confidence_interval(alpha: float,
                                  repetition: int,
                                  time_list: list) -> float:
    average_time = sum(time_list) / repetition
    standard_deviation = sqrt((1 / (repetition - 1)) * (
        sum([(t - average_time) ** 2 for t in time_list])))
    return alpha * standard_deviation / sqrt(repetition)


class Reporter:
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

    def __init__(self,
                 functions: list[Callable[[str, str], Union[tuple, int]]],
                 comparing_parameters: list[tuple[str, str, str]],
                 repetition: int):
        for e in functions:
            if not hasattr(e, "__call__"):
                raise TypeError(f"{e} is not a function")
        if repetition not in self._alpha_dict:
            raise ValueError(
                f'You can only set the following repeat values\n'
                f'{", ".join([str(x) for x in self._alpha_dict.keys()])}')
        self._tester = Tester(functions, comparing_parameters, repetition,
                              'intermediate_results.txt')
        self._substring_finders = functions
        self._repetition = repetition
        self._all_statistics = None

    def generate_statistics(self):
        self._all_statistics = self._tester.test()
        self._generate_report_in_md_format()
        self._compute_data_for_graphs()

    def _generate_report_in_md_format(self):
        finders_docs = [
            self.parse_documentation(e)
            for e in map(lambda x: x.__doc__, self._substring_finders)
        ]
        report_data = [e for e in zip(*[e for e in finders_docs])]
        report = [
            f'|Parameter name|{"|".join(report_data[0])}|',
            "|-" * (len(self._substring_finders) + 1) + "|",
            f'|Time complexity|{"|".join(report_data[1])}|',
            f'|Memory complexity|{"|".join(report_data[2])}|',
        ]
        stats_lines = [f"|{'|'.join(e)}|" for e in self._all_statistics]
        report.extend(stats_lines)
        with open("report.md", "w") as f:
            f.write("\n".join(report))

    @staticmethod
    def parse_documentation(doc: str) -> list:
        name = re.search("(?<=Name:).+", doc)[0].strip()
        time_complexity = re.search("(?<=Time complexity:).+", doc)[0].strip()
        memory_complexity = re.search("(?<=Memory complexity:).+", doc)[
            0].strip()
        return [name, time_complexity, memory_complexity]

    def _compute_data_for_graphs(self):
        float_pattern = re.compile(r'\d+\.\d+')
        function_name_pattern = re.compile("|".join(
            map(lambda x: x.__name__, self._substring_finders)))
        with open(self._tester.path_to_save, mode='r', encoding='utf-8') as f:
            data = f.readlines()
            for i in range(len(data)):
                function_name = re.search(function_name_pattern, data[i])
                if function_name is None:
                    continue
                time_list = [float(x) for x in
                             re.findall(float_pattern, data[i])]
                confidence_interval = calculate_confidence_interval(
                    self._alpha_dict[self._repetition], self._repetition,
                    time_list)
                average_time_of_work = sum(time_list) / len(time_list)
                data[i] \
                    = '{} confidence interval: {}, average time: {}\n'.format(
                    function_name[0], confidence_interval,
                    average_time_of_work)
        save_intermediate_results(data, 'w', self._tester.path_to_save)


class Tester:
    def __init__(self,
                 functions: list[Callable[[str, str], Union[tuple, int]]],
                 comparing_parameters: list[tuple[str, str, str]],
                 repeats: int,
                 path_to_save: str):
        self._comparing_parameters = comparing_parameters
        self._repeats = repeats
        self._functions = functions
        self.path_to_save = path_to_save

    def test(self):
        stats = []
        for text_path, test_substring, statistic_name in self._comparing_parameters:
            with open(text_path, encoding="utf-8") as f:
                stats.append(
                    self._get_base_statistics(f.read(), test_substring,
                                              statistic_name))
        return stats

    def _get_base_statistics(
            self, test_text: str, test_substring: str, statistic_name: str
    ) -> list[str]:
        save_intermediate_results(statistic_name, 'a', self.path_to_save)
        statistics = [statistic_name]
        for finder in self._functions:
            finder(test_text, test_substring)
            finder(test_text, test_substring)
            time_of_work = []
            for _ in range(self._repeats):
                start_time = default_timer()
                finder(test_text, test_substring)
                end_time = default_timer()
                time_of_work.append(end_time - start_time)
            statistics.append(f'{(sum(time_of_work) / self._repeats):0.6f}')
            save_intermediate_results(str([finder.__name__] + time_of_work),
                                      'a', self.path_to_save)
        return statistics
