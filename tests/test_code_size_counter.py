import os
import unittest
from pathlib import Path

from code_size_counter.code_size_counter import CodeSizeCounter
from code_size_counter.file_tools import FileSetSize


class TestCodeSizeCounter(unittest.TestCase):
    """
    class containing tests for calculate_size method of CodeSizeCounter class
    """

    def test_calculate_size_simple(self):
        """
        a simple test case - no items to exclude, single file extension
        """
        code_size_counter = CodeSizeCounter(
            os.path.join(_get_tests_dir(), "simple-test-dir"), ("txt",), False, ()
        )
        code_size = code_size_counter.calculate_size()

        expected_result = {"txt": FileSetSize(3, 35, 2374)}

        self.assertDictEqual(expected_result, code_size)

    def test_calculate_size_complex(self):
        """
        complex test case - allowed multiple (however not all) file extensions, excluding folders & files
        """
        excluded_items = map(
            lambda ex: os.path.join(_get_tests_dir(), "complex-test-dir", ex),
            [os.path.join("src", "module2", "main.py"), "virtualenv"],
        )

        code_size_counter = CodeSizeCounter(
            os.path.join(_get_tests_dir(), "complex-test-dir"),
            ("py", "yml", "md", "txt"),
            False,
            tuple(excluded_items),
        )
        code_size = code_size_counter.calculate_size()

        expected_result = {
            "py": FileSetSize(11, 270, 8511),
            "yml": FileSetSize(1, 36, 1187),
            "md": FileSetSize(1, 3, 144),
        }

        self.assertDictEqual(expected_result, code_size)
        # self.assertEqual(13, code_size.total_files)
        # self.assertEqual(9842, code_size.total_size)
        # self.assertEqual(309, code_size.total_lines)

    def test_calculate_size_exclude_directories(self):
        """
        test case with excluding directories
        """
        excluded_directories = map(
            lambda ex: os.path.join(_get_tests_dir(), "exclude-test-dir", ex),
            [os.path.join("dir", "dir-ex2"), "dir-ex"],
        )

        code_size_counter = CodeSizeCounter(
            os.path.join(_get_tests_dir(), "exclude-test-dir"),
            ("py",),
            False,
            tuple(excluded_directories),
        )
        code_size = code_size_counter.calculate_size()

        expected_result = {"py": FileSetSize(2, 4, 104)}

        self.assertDictEqual(expected_result, code_size)

    def test_calculate_size_no_matching_files(self):
        """
        test case that doesn't find any suitable files
        """
        code_size_counter = CodeSizeCounter(
            os.path.join(_get_tests_dir(), "no-matching-files-test-dir"),
            ("py",),
            False,
            (os.path.join(_get_tests_dir(), "no-matching-files-test-dir", "dir-py"),),
        )
        code_size = code_size_counter.calculate_size()

        self.assertDictEqual({}, code_size)


def _get_tests_dir():
    """
    get path to /tests directory
    """
    return Path(__file__).parent.absolute()


if __name__ == "__main__":
    unittest.main()
