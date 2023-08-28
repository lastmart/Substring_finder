from timeit import default_timer
from collections import namedtuple, defaultdict
from typing import Union, Callable, Pattern
import matplotlib.pyplot as plt
from math import sqrt
import re

Documentation = namedtuple('Documentation',
                           ['name', 'time_complexity', 'memory_complexity'])
TestingResult = namedtuple('TestingResult',
                           ['name', 'confidence_interval', 'average_time'])
PatternContent = namedtuple('PatternContent', ['number', 'content'])


def save_intermediate_results(data: Union[list, str],
                              mode: str,
                              path_to_save: str) -> None:
    with open(path_to_save, encoding='utf-8', mode=mode) as f:
        if isinstance(data, str):
            f.write(f'{data}\n')
        elif isinstance(data, list):
            f.writelines(data)
        else:
            raise ValueError(f'Incorrect type to save: {type(data)}')


def calculate_confidence_interval(alpha: float,
                                  repetition: int,
                                  time_list: list) -> float:
    average_time = sum(time_list) / repetition
    standard_deviation = sqrt((1 / (repetition - 1)) * (
        sum([(t - average_time) ** 2 for t in time_list])))
    return alpha * standard_deviation / sqrt(repetition)


def determine_pattern_for_string(patterns: list[Pattern], data: str) \
        -> Union[PatternContent, None]:
    for i in range(len(patterns)):
        searching = re.search(patterns[i], data)
        if searching:
            return PatternContent(i, searching[0])
    return None


class Point:
    def __init__(self, name: str, x: float, y: float, amplitude: float):
        self.name = name
        self.x = x
        self.y = y
        self.amplitude = amplitude

    def get_y_range(self):
        return [self.y - self.amplitude, self.y + self.amplitude]

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value: int):
        if value < 0:
            raise ValueError(f'Amplitude can not be negative: {value}')
        self._amplitude = value

    def __str__(self):
        return f'{self.name}\nx: {self.x}, y: {self.y}, amplitude: {self.amplitude}'


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
                 repetition: int,
                 groups_patterns: list[Pattern] = None):
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
        self._groups_patterns = groups_patterns

    def generate_statistics(self):
        self._all_statistics = self._tester.test()
        self._generate_report_in_md_format()
        self._compute_data_for_graphs()
        if self._groups_patterns:
            for data_class in self.parse_data_for_graphs(
                    self._substring_finders,
                    self._tester.path_to_save,
                    self._groups_patterns):
                for key, points in data_class.items():
                    graph_builder = GraphBuilder(points)
                    graph_builder.build_graphs()

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
    def parse_documentation(doc: str) -> Documentation:
        name = re.search("(?<=Name:).+", doc)[0].strip()
        time_complexity = re.search("(?<=Time complexity:).+", doc)[0].strip()
        memory_complexity = re.search("(?<=Memory complexity:).+", doc)[
            0].strip()
        return Documentation(name, time_complexity, memory_complexity)

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

    @staticmethod
    def parse_data_for_graphs(
            substring_finders: list[Callable[[str, str], Union[tuple, int]]],
            file_path: str,
            groups_patterns: list[Pattern]):
        confidence_interval_pattern = re.compile(
            r'(?<=confidence interval:\s)[0-9.]+')
        function_name_pattern = re.compile("|".join(
            map(lambda x: x.__name__, substring_finders)))
        average_time_pattern = re.compile(r'(?<=average time:\s)[0-9.]+')

        data_classes = [defaultdict() for _ in range(len(groups_patterns))]
        current_group_name = None
        current_group_number = None

        with open(file_path, mode='r') as f:
            for line in f:
                group = determine_pattern_for_string(groups_patterns, line)
                if group:
                    current_group_name = group.content
                    current_group_number = group.number
                    continue
                res = Reporter.parse_testing_results(line,
                                                     function_name_pattern,
                                                     confidence_interval_pattern,
                                                     average_time_pattern)
                current_dict = data_classes[current_group_number]
                if not current_dict.get(current_group_name):
                    current_dict[current_group_name] = []
                current_dict[current_group_name].append(
                    Point(name=res.name,
                          x=len(current_dict[current_group_name]),
                          y=res.average_time,
                          amplitude=res.confidence_interval)
                )

        return data_classes

    @staticmethod
    def parse_testing_results(data: str,
                              function_name_pattern: Pattern,
                              confidence_interval_pattern: Pattern,
                              average_time_pattern: Pattern) -> TestingResult:
        name = re.search(function_name_pattern, data)[0].strip()
        confidence_interval = \
            re.search(confidence_interval_pattern, data)[0].strip()
        average_time = re.search(average_time_pattern, data)[0].strip()
        return TestingResult(name, float(confidence_interval),
                             float(average_time))


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


class GraphBuilder:
    def __init__(self, points: list[Point]):
        self._points = points

    def build_graphs(self):
        for point in self._points:
            pass
