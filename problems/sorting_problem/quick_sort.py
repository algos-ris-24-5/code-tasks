import random

_ERROR_TEMPLATE = "Переданы несравнимые экземпляры классов '{0}' и '{1}'"

def quick_sort(items):
    """Сортирует переданный список по возрастанию с использованием алгоритма
    быстрой сортировки (Quick Sort).

    Реализация использует принцип "разделяй и властвуй" и схему разбиения Хоара,
    является рекурсивной. Возвращает новый список, исходный список не изменяется.

    :param items: Список элементов для сортировки.
    :type items: list
    :return: Новый список, содержащий отсортированные элементы.
    :rtype: list
    :raises TypeError: Если элементы списка несравнимы между собой.
    """
    _validate_comparable(items)

    arr = items.copy()
    if len(arr) <= 1:
        return arr

    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _validate_comparable(items):
    if not items: 
        return

    first_item = items[0]
    for item in items:
        try:
            is_comparable = item < first_item
        except TypeError:
            type_a = type(item).__name__
            type_b = type(first_item).__name__

            if type_a < type_b:
                type_a, type_b = type_b, type_a

            raise TypeError(_ERROR_TEMPLATE.format(type_a, type_b))


def _partition(arr, left, right):
    pivot_idx = random.randint(left, right)
    pivot = arr[pivot_idx]

    left_idx = left
    right_idx = right

    while True:
        while arr[left_idx] < pivot:
            left_idx += 1
        while arr[right_idx] > pivot:
            right_idx -= 1

        if left_idx >= right_idx:
            return right_idx

        arr[left_idx], arr[right_idx] = arr[right_idx], arr[left_idx]
        left_idx += 1
        right_idx -= 1


def _quick_sort(arr, left, right):
    if left < right:
        pivot_index = _partition(arr, left, right)
        _quick_sort(arr, left, pivot_index)
        _quick_sort(arr, pivot_index + 1, right)


def main():
    print("Пример быстрой сортировки")
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print(f"Исходный массив: {items}")
    print(f"Отсортированный массив: {quick_sort(items)}")


if __name__ == "__main__":
    main()
