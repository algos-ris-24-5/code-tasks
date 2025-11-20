def _data_validation_tridiagonal_determinant(matrix: list[list[int]]) -> None:
    """
    Внутренняя функция для проверки корректности ввода данных в трехдиагональную матрицу
    """
    pass

def _get_reduced_matrix(matrix: list[list[int]], row: int, column: int) -> list[list[int]]:
    """
    Функция для вычисления матрицы с вычеркнутым столбцом и строкой
    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :param row: Вычеркиваемый ряд из исходной матрицы.
    :param column: Вычеркиваемый столбец из исходной матрицы.

    :return: Полученная матрица.
    """
    pass

def _get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """
    Внутренняя функция вычисления определителя трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    if len(matrix) == 1:
        return matrix[0][0]
    
    det = 0


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    
    _data_validation_tridiagonal_determinant(matrix)
    return _get_tridiagonal_determinant(matrix)


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
