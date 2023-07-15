import substring_finder
from report import Reporter

if __name__ == '__main__':
    substring_finders = [
        substring_finder.simplest_str_finder,
        substring_finder.KMP_algorithm,
        substring_finder.z_function_finder,
        substring_finder.BMH_algorithm
    ]
    reporter = Reporter(substring_finders)
    reporter.make_stats()
