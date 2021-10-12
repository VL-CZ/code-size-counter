import os
import unittest
from pathlib import Path

from src.code_size_counter import CodeSizeCounter


class TestCodeSizeCounter(unittest.TestCase):
    """
    class containing tests for calculate_size method of CodeSizeCounter class
    """

    def test_calculate_size_simple(self):
        """
        a simple test case - no items to exclude, single file extension
        """
        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'simple-test-dir'), ('txt',), False, ())
        code_size = code_size_counter.calculate_size()

        self.assertEqual(3, code_size.total_files)
        self.assertEqual(2374, code_size.total_size)
        self.assertEqual(35, code_size.total_lines)

    def test_calculate_size_complex(self):
        """
        complex test case - allowed multiple (however not all) file extensions, excluding folders & files
        """
        excluded_items = map(lambda ex: os.path.join(_get_tests_dir(), 'complex-test-dir', ex),
                             [os.path.join('src', 'module2', 'main.py'), 'virtualenv'])

        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'complex-test-dir'), ('py', 'yml', 'md'),
                                            False, tuple(excluded_items))
        code_size = code_size_counter.calculate_size()

        self.assertEqual(13, code_size.total_files)
        self.assertEqual(9842, code_size.total_size)
        self.assertEqual(309, code_size.total_lines)

    def test_calculate_size_exclude_directories(self):
        """
        test case with excluding directories
        """
        excluded_directories = map(lambda ex: os.path.join(_get_tests_dir(), 'exclude-test-dir', ex),
                                   [os.path.join('dir', 'dir-ex2'), 'dir-ex'])

        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'exclude-test-dir'), ('py',), False,
                                            tuple(excluded_directories))
        code_size = code_size_counter.calculate_size()

        self.assertEqual(2, code_size.total_files)
        self.assertEqual(104, code_size.total_size)
        self.assertEqual(4, code_size.total_lines)

    def test_calculate_size_no_matching_files(self):
        """
        test case that doesn't find any suitable files
        """
        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'no-matching-files-test-dir'), ('py',),
                                            False,
                                            (os.path.join(_get_tests_dir(), 'no-matching-files-test-dir', 'dir-py'),)
                                            )
        code_size = code_size_counter.calculate_size()

        self.assertEqual(0, code_size.total_files)
        self.assertEqual(0, code_size.total_size)
        self.assertEqual(0, code_size.total_lines)


def _get_tests_dir():
    """
    get path to /tests directory
    """
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    unittest.main()
