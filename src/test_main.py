import main
import unittest


class TestCalc(unittest.TestCase):

    def add_test(self):
        result = main.add(10, 5)
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()

