import os
import unittest
from pathlib import Path

from src.code_size_counter import CodeSizeCounter


class TestCodeSizeCounter(unittest.TestCase):
    """
    class containing tests for CodeSizeCounter class
    """

    def test_calculate_size_simple(self):
        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'simple-test-dir'), ('txt',), False, ())
        code_size = code_size_counter.calculate_size()

        self.assertEqual(3, code_size.total_files)
        self.assertEqual(2374, code_size.total_size)
        self.assertEqual(35, code_size.total_lines)

    def test_calculate_size_complex(self):
        pass

    def test_calculate_size_exclude_files(self):
        excluded_directories = map(lambda ex: os.path.join(_get_tests_dir(), 'exclude-test-dir', ex),
                                   [os.path.join('dir', 'dir-ex2'), 'dir-ex'])

        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'exclude-test-dir'), ('py',), False,
                                            tuple(excluded_directories))
        code_size = code_size_counter.calculate_size()

        self.assertEqual(2, code_size.total_files)
        self.assertEqual(104, code_size.total_size)
        self.assertEqual(4, code_size.total_lines)

    def test_calculate_size_no_matching_files(self):
        pass


def _get_tests_dir():
    """
    get path to /tests directory

    :return: path to /tests directory
    """
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    unittest.main()
