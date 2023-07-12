from timeit import default_timer
import substring_finder


class Reporter:
    def __init__(self, functions):
        self.substring_finders = functions
        self.all_statistics = []

    def make_stats(self):
        stats = self.get_stats()
        finders_docs = [e for e in map(lambda x: x.__doc__, self.substring_finders)]
        a = [e for e in zip(map(lambda x: x.split('\n'), finders_docs))]
        report = [
            f'|comparing parameter|{"|".join(map(lambda x: x.__name__, self.substring_finders))}|',
            '|-' * (len(self.substring_finders) + 1) + '|',
            f'|Asymptotics|{"|".join(map(lambda x: x.__doc__, self.substring_finders))}|'
            ]
        stats_lines = [f"|{'|'.join(e)}|" for e in stats]
        for e in stats_lines:
            report.append(e)
        with open('report.md', 'w') as f:
            f.write('\n'.join(report))

    def get_stats(self):
        comparing_parameters = filter(lambda x: x[0] != '_', dir(Reporter))
        for parameter in comparing_parameters:
            if parameter in ["make_stats", "get_stats"]:
                continue
            self.all_statistics.append(getattr(Reporter, parameter)(self))
        return self.all_statistics

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
            for _ in range(1000):
                finder(test_text, test_substring)
            statistics.append(str(default_timer() - start_time))
        return statistics


if __name__ == '__main__':
    substring_finders = [
        substring_finder.simplest_str_finder,
        substring_finder.KMP_algorithm
    ]
    reporter = Reporter(substring_finders)
    reporter.make_stats()
