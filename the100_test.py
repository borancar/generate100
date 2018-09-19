import sys
import unittest
try:
    from unittest import mock
except ImportError:
    print("Need Python3 for mock testing")
    sys.exit(1)

import the100


class _ReadTester(object):
    def __init__(self, contents, test):
        self.contents = contents
        self.test = test
        self.read_called = 0

    def read(self, *args, **kwargs):
        # Make sure the read is for full file
        self.test.assertEqual(len(args), 0)
        self.test.assertEqual(len(kwargs), 0)
        self.read_called += 1
        return self.contents


class _FileTester(object):
    def __init__(self, name, mode, contents, test):
        self.name = name
        self.mode = mode
        self.contents = contents
        self.test = test
        self.read_tester = _ReadTester(self.contents, self.test)

    def __enter__(self):
        return self.read_tester

    def __exit__(self, type, value, traceback):
        pass


class TestThe100(unittest.TestCase):

    def test_random_file(self):
        for i in range(1, 101):
            contents = the100.random_file(i)
            self.assertGreaterEqual(len(contents), 1)
            self.assertLessEqual(len(contents), 65)

    def test_mod5_file(self):
        self.assertEqual(the100.mod5_file(5), "This is every 5th file!")

    def test_mod7_file(self):
        file_testers = {}

        def _mock_open(name, mode):
            # Mock files with the contents just being the name
            file_testers[name] = _FileTester(name,
                                             mode,
                                             contents=name,
                                             test=self)
            return file_testers[name]

        # Last divisible by 7 is 98
        contents = the100.mod7_file(98, open_fn=_mock_open)

        # Check that there were 97 unique files opened
        # and that each one was read fully once
        self.assertEqual(len(file_testers.keys()), 97)
        for name, file_tester in file_testers.items():
            self.assertEqual(file_tester.read_tester.read_called, 1)

        # Check there are 97 lines in the result
        self.assertEqual(len(contents.split("\n")), 97)

    @mock.patch("the100.mod7_file")
    @mock.patch("the100.mod5_file")
    @mock.patch("the100.random_file")
    def test_evaluate_rules(self, patched_random, patched_mod5, patched_mod7):
        for i in range(1, 101):
            the100.evaluate_rules(i)

        # There are 20 numbers divisible by 5 in the range [1, 100], 2 of
        # which are also divisible by 7 (45 and 70)
        self.assertEqual(patched_mod5.call_count, 18)
        # There are 14 numbers divisible by 7 in the range [1, 100]
        self.assertEqual(patched_mod7.call_count, 14)
        # 100 - 18 - 14 = 68
        self.assertEqual(patched_random.call_count, 68)


if __name__ == "__main__":
    unittest.main()
