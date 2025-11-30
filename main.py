def _is_valid_tridiagonal(m):
    """Внутренняя проверка: квадратная + трёхдиагональная + постоянные диагонали."""
    if not m or not m[0]:
        raise ValueError("Матрица пустая или некорректная")

    n = len(m)
    if any(len(row) != n for row in m):
        raise ValueError("Матрица должна быть квадратной")

    # Проверка трёхдиагональности
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and m[i][j] != 0:
                raise ValueError("Матрица не является трёхдиагональной")

    # Проверка постоянства диагоналей
    if n >= 1:
        a0 = m[0][0]
        for i in range(n):
            if m[i][i] != a0:
                raise ValueError("Главная диагональ должна быть постоянной")

    if n >= 2:
        b0 = m[0][1]
        c0 = m[1][0]
        for i in range(n-1):
            if m[i][i+1] != b0:
                raise ValueError("Верхняя диагональ должна быть постоянной")
        for i in range(1, n):
            if m[i][i-1] != c0:
                raise ValueError("Нижняя диагональ должна быть постоянной")


def _minor(matrix, k):
    """Минор: удаляем первые k строк и столбцов."""
    return [row[k:] for row in matrix[k:]]


def _det_rec(m):
    """Рекурсивный расчёт определителя по специальной формуле для таких матриц."""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    a = m[0][0]
    b = m[0][1]
    c = m[1][0]

    return a * _det_rec(_minor(m, 1)) - b * c * _det_rec(_minor(m, 2))


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """
    Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :return: значение определителя.
    """
    _is_valid_tridiagonal(matrix)
    return _det_rec(matrix)


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)
    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()