import unittest

from problems.sorting_problem.quick_sort import quick_sort
from tests.problems.sorting_problem.test_abstract import TestAbstractSorter


class TestSomeSort(unittest.TestCase, TestAbstractSorter):
    """Набор тестов для проверки метода быстрой сортировки."""

    sort_method = lambda _, items: quick_sort(items)


if __name__ == "__main__":
    unittest.main()
