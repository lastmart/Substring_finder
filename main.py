import substring_finder
from report import Reporter


if __name__ == '__main__':
    substring_finders = [
        substring_finder.brute_force,
        substring_finder.KMP_algorithm,
        substring_finder.z_function_finder,
        substring_finder.BMH_algorithm,
        substring_finder.AC_algorithm,
    ]
    reporter = Reporter(substring_finders, 51)
    # reporter.generate_statistics()
    reporter._calculate_confidence_interval_for_each_result()
