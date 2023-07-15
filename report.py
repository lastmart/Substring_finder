from timeit import default_timer
import re


class Reporter:
    def __init__(self, functions: list):
        for e in functions:
            if not hasattr(e, '__call__'):
                raise TypeError(f'{e} is not a function')
        self.substring_finders = functions
        self.all_statistics = []

    def make_stats(self):
        stats = self.get_stats()
        finders_docs = [self.parse_documentation(e) for e in
                        map(lambda x: x.__doc__, self.substring_finders)]
        report_data = [e for e in zip(*[e for e in finders_docs])]
        report = [
            f'|Parameter name|{"|".join(report_data[0])}|',
            '|-' * (len(self.substring_finders) + 1) + '|',
            f'|Time complexity|{"|".join(report_data[1])}|',
            f'|Memory complexity|{"|".join(report_data[2])}|'
        ]
        stats_lines = [f"|{'|'.join(e)}|" for e in stats]
        for e in stats_lines:
            report.append(e)
        with open('report.md', 'w') as f:
            f.write('\n'.join(report))

    def get_stats(self):
        comparing_parameters = [
            self.get_statistics_of_duplicate_data,
            self.get_statistics_of_non_duplicate_data
        ]
        for parameter in comparing_parameters:
            self.all_statistics.append(parameter())
        return self.all_statistics

    @staticmethod
    def parse_documentation(doc: str) -> list:
        name = re.search('(?<=Name:).+', doc)[0].strip()
        time_complexity = re.search('(?<=Time complexity:).+', doc)[0].strip()
        memory_complexity = re.search('(?<=Memory complexity:).+', doc)[
            0].strip()
        return [name, time_complexity, memory_complexity]

    def get_statistics_of_duplicate_data(self):
        test_text = '''
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Van. Hello my dear Billy. Hello my dear Dungeon
        Hello my dear Sun
        '''
        test_substring = 'Hello my dear Sun'
        return self._get_base_statistics(test_text, test_substring,
                                         'Many similar lines')

    def get_statistics_of_non_duplicate_data(self):
        test_text = '''
        ASDFGHJKL:"ZXCVBNM<>?ASDFGHJKL:"ZXCVBNM<>?
        asdfghjkl;'zxcvbnm,./asdfghjkl;'zxcvbnm,./
        QWERTYUIOP{}QWERTYUIOP{}QWERTYUIOP{}
        1234567890123456789012345678901234567890
        1234567890123456789012345678901234567890
        qwertyuiop[]
        '''
        test_substring = 'qwerty'
        return self._get_base_statistics(test_text, test_substring,
                                         'None similar lines')

    def _get_base_statistics(self, test_text: str, test_substring: str,
                             statistic_name: str):
        statistics = [statistic_name]
        for finder in self.substring_finders:
            start_time = default_timer()
            for _ in range(100000):
                finder(test_text, test_substring)
            statistics.append(str(default_timer() - start_time))
        return statistics
