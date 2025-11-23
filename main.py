def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    _validate_matrix(matrix)
    return _determinant_recursive(matrix)


def _determinant_recursive(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for idx, item in enumerate(matrix[0]):
        det += (
            item
            * (-1) ** idx 
            * _determinant_recursive(_get_reduced_matrix(matrix, 0, idx))
        )
    return det


def _get_reduced_matrix(matrix, row_idx, col_idx):
    reduced = []
    for i in range(len(matrix)):
        if i == row_idx:
            continue
        new_row = []
        for j in range(len(matrix[i])):
            if j == col_idx:
                continue
            new_row.append(matrix[i][j])
        reduced.append(new_row)
    return reduced


def _validate_matrix(matrix):
    if matrix is None:
        raise Exception("Matrix is None")

    if not isinstance(matrix, list):
        raise Exception("Matrix is not a list")

    n = len(matrix)
    if n == 0:
        raise Exception("Matrix is empty")

    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise Exception(f"Row {i} is not a list")
        if len(row) != n:
            raise Exception("Matrix is not square")
        for j, elem in enumerate(row):
            if not isinstance(elem, int):
                raise Exception(f"Element at ({i}, {j}) is not an integer")


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
