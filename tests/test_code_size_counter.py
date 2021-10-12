import os
import unittest
from pathlib import Path

from src.code_size_counter import CodeSizeCounter


class TestCodeSizeCounter(unittest.TestCase):

    def test_calculate_size_simple(self):
        code_size_counter = CodeSizeCounter(os.path.join(_get_tests_dir(), 'simple-test-dir'), ('txt',), False,
                                            [])
        code_size = code_size_counter.calculate_size()

        self.assertEqual(3, code_size.total_files)
        self.assertEqual(2374, code_size.total_size)
        self.assertEqual(35, code_size.total_lines)


def _get_tests_dir():
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    unittest.main()
