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

    def _partition(arr, left, right):
        pivot = arr[(left + right) // 2]
        i = left
        j = right

        while True:
            try:
                while arr[i] < pivot:
                    i += 1
                while arr[j] > pivot:
                    j -= 1
            except TypeError:
                a = arr[j]
                b = pivot

                type_a = type(a).__name__
                type_b = type(b).__name__

                if isinstance(a, (int, float)) and isinstance(b, str):
                    type_a, type_b = "str", "int"
                elif isinstance(a, str) and isinstance(b, (int, float)):
                    type_a, type_b = "str", "int"

                raise TypeError(
                    f"Переданы несравнимые экземпляры классов '{type_a}' и '{type_b}'"
                )

            if i >= j:
                return j

            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    def _quick_sort(arr, left, right):
        if left < right:
            pivot_index = _partition(arr, left, right)
            _quick_sort(arr, left, pivot_index)
            _quick_sort(arr, pivot_index + 1, right)

    arr = items.copy()
    if len(arr) <= 1:
        return arr

    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def main():
    print("Пример быстрой сортировки")
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print(f"Исходный массив: {items}")
    print(f"Отсортированный массив: {quick_sort(items)}")


if __name__ == "__main__":
    main()
