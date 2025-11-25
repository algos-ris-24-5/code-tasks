def _data_validation_tridiagonal_determinant(matrix: list[list[int]]) -> None:
    """
    Внутренняя функция для проверки корректности ввода данных в трехдиагональную матрицу
    """
    if not matrix or not isinstance(matrix, list):
        raise Exception("Incorrect input data type")

    number_rows = len(matrix)
    for row in matrix:
        if len(row) != number_rows:
            raise Exception("A rectangular matrix or an echelon matrix is ​​transmitted")

    is_incorrect_filled_in = False
    if number_rows > 2:
        for idx, el in enumerate(matrix[0]):
            if idx > 1 and el != 0:
                is_incorrect_filled_in = True
                break
        cur_start_index = 0
        for row_index in range(1, number_rows - 1):
            for idx, el in enumerate(matrix[row_index]):
                if idx not in range(cur_start_index, cur_start_index + 3) and el != 0:
                    is_incorrect_filled_in = True
                    break
            cur_start_index += 1
        for idx, el in enumerate(matrix[number_rows - 1]):
            if idx < number_rows - 2 and el != 0:
                is_incorrect_filled_in = True
                break
    if is_incorrect_filled_in:
        raise Exception("A normal matrix was transmitted, not a tridiagonal matrix")

    is_inconsistent_data = False
    for i in range(number_rows - 1):
        if matrix[i][i] != matrix[i + 1][i + 1]:
            is_inconsistent_data = True
            break
    for i in range(number_rows - 2):
        if (
            matrix[i + 1][i] != matrix[i + 2][i + 1]
            or matrix[i][i + 1] != matrix[i + 1][i + 2]
        ):
            is_inconsistent_data = True
            break
    if is_inconsistent_data:
        raise Exception("The diagonals contain non-coinciding values")


def _get_reduced_matrix(
    matrix: list[list[int]], row: int, column: int
) -> list[list[int]]:
    """
    Функция для вычисления матрицы с вычеркнутым столбцом и строкой
    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :param row: Вычеркиваемый ряд из исходной матрицы.
    :param column: Вычеркиваемый столбец из исходной матрицы.

    :return: Полученная матрица.
    """

    created_matrix: list[list[int]] = []
    curi = -1
    for i in range(len(matrix)):
        if i == row:
            continue
        curi += 1
        created_matrix.append([])
        for j in range(len(matrix)):
            if j == column:
                continue
            created_matrix[curi].append(matrix[i][j])

    return created_matrix


def _get_tridiagonal_determinant(a: int, b: int, c: int, size_matr: int) -> int:
    """
    Внутренняя функция вычисления определителя трехдиагональной целочисленной квадратной матрицы.
    :param a: элемент главной диагонали
    :param b: элемент верхней диагонали
    :param c: элемент нижней диагонали

    :return: значение определителя.
    """
    if size_matr == 1:
        return a
    if size_matr == 2:
        return a**2 - (b * c)

    return a * _get_tridiagonal_determinant(
        a, b, c, size_matr - 1
    ) - b * c * _get_tridiagonal_determinant(a, b, c, size_matr - 2)


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """

    _data_validation_tridiagonal_determinant(matrix)

    if len(matrix) == 1:
        return matrix[0][0]

    main_diag = matrix[0][0]
    upper_diag = matrix[0][1]
    lower_diag = matrix[1][0]
    return _get_tridiagonal_determinant(main_diag, upper_diag, lower_diag, len(matrix))


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
