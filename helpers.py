from typing import Callable, Union, Pattern
from timeit import default_timer
import matplotlib.pyplot as plt
from collections import namedtuple
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
    def __init__(self, data: dict[str, list[Point]], path_to_save: str):
        self._data = data
        self.path_to_save = path_to_save

    def build_graphs(self):
        grid_size = self.get_grid_size(len(self._data.keys()))
        figure = plt.figure(figsize=(40, 30))
        current_number = 1
        for key, points in self._data.items():
            ax = figure.add_subplot(*grid_size, current_number)
            ax.set_title(key, fontsize=30)
            for point in points:
                ax.plot(point.x, point.y, marker='o', color='red')
                ax.plot([point.x] * 2, point.get_y_range(), linestyle='-',
                        color='red', alpha=0.6)
            current_number += 1
            plt.xticks(list(map(lambda p: p.x, points)),
                       list(map(lambda p: p.name, points)), fontsize=20)
        figure.savefig(self.path_to_save)
        figure.show()

    @staticmethod
    def get_grid_size(number: int) -> tuple[int, int]:
        x = y = round(sqrt(number))
        x = x if x * y >= number or x * (y + 1) >= number else x + 1
        y = y if x * y >= number or (x + 1) * y >= number else y + 1
        return x, y
