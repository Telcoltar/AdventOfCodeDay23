from unittest import TestCase

from main import solution_part_1, solution_part_2


class Test(TestCase):
    def test_solution_part_1(self):
        self.assertEqual("92658374", solution_part_1("testData.txt", 10))
        self.assertEqual("67384529", solution_part_1("testData.txt", 100))

    def test_solution_part_2(self):
        self.assertEqual(149245887792, solution_part_2("testData.txt", 10000000))
