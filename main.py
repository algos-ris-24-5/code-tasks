from problems.sorting_problem.quick_sort import quick_sort

"""В файле расположен пример использования метода быстрой сортировки.
Метод расположен в problems/sorting_problem/quick_sort.py
"""


def main():
    print("Пример быстрой сортировки")
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print(f"Исходный массив: {items}")
    print(f"Отсортированный массив: {quick_sort(items)}")


if __name__ == "__main__":
    main()
