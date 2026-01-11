PATH_LENGTH_ERROR_MSG = "Длина маршрута должна быть целым положительным числом"
"""Сообщение об ошибке при некорректном значении параметра Длина маршрута"""

NOT_INT_VALUE_TEMPL = "Параметр {0} Не является целым числом"
"""Шаблон сообщения об ошибке при нечисловом значении параметра"""

NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
"""Шаблон сообщения об ошибке при отрицательном значении параметра"""

N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"
"""Сообщение об ошибке при значении параметра n меньше чем k"""


def _is_strict_int(value) -> bool:
    """Проверяет, что значение является именно int (не bool)."""
    return type(value) is int


def get_triangle_path_count(length: int) -> int:
    """Вычисляет количество замкнутых маршрутов заданной длины между тремя
    вершинами треугольника A, B и C. Маршруты начинаются и оканчиваются в
    вершине A vertex. Допустимыми являются все пути между различными вершинами.
    :param length: Длина маршрута.
    :raise ValueError: Если длина маршрута не является целым положительным
    числом.
    :return: Количество маршрутов.
    """
    if not _is_strict_int(length) or length <= 0:
        raise ValueError(PATH_LENGTH_ERROR_MSG)

    def a(n: int) -> int:
        if n == 1:
            return 0
        return b(n - 1) + c(n - 1)

    def b(n: int) -> int:
        if n == 1:
            return 1
        return a(n - 1) + c(n - 1)

    def c(n: int) -> int:
        if n == 1:
            return 1
        return a(n - 1) + b(n - 1)

    return a(length)


def binomial_coefficient(n: int, k: int, use_rec=False) -> int:
    """Вычисляет биномиальный коэффициент из n по k.
    :param n: Количество элементов в множестве, из которого производится выбор.
    :param k: Количество элементов, которые нужно выбрать.
    :param use_rec: Использовать итеративную или рекурсивную реализацию функции.
    :raise ValueError: Если параметры не являются целыми неотрицательными
    числами или значение параметра n меньше чем k.
    :return: Значение биномиального коэффициента.
    """
    if not _is_strict_int(n):
        raise ValueError(NOT_INT_VALUE_TEMPL.format("n"))
    if not _is_strict_int(k):
        raise ValueError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)

    if k == 0 or k == n:
        return 1
    if k == 1:
        return n

    k_eff = min(k, n - k)

    def rec(nn: int, kk: int) -> int:
        if kk == 0 or kk == nn:
            return 1
        if kk == 1:
            return nn
        return (nn * rec(nn - 1, kk - 1)) // kk

    if use_rec:
        return rec(n, k_eff)

    res = 1
    for i in range(1, k_eff + 1):
        res = ((n - k_eff + i) * res) // i
    return res


def main():
    n = 10
    print(f"Количество маршрутов длиной {n} = {get_triangle_path_count(n)}")

    n = 30
    k = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k),
    )
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k, use_rec=True),
    )


if __name__ == "__main__":
    main()
