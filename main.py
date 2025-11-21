def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    validate_matrix(matrix)

    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for idx, item in enumerate(matrix[0]):
        det += (
            item
            * (-1) ** idx
            * calculate_determinant(get_reduced_matrix(matrix, 0, idx))
        )
    return det


def get_reduced_matrix(matrix, row_idx, col_idx):
    n = len(matrix)
    result = []
    for i in range(n):
        if i != row_idx:
            new_row = []
            for j in range(n):
                if j != col_idx:
                    new_row.append(matrix[i][j])
            result.append(new_row)
    return result


def validate_matrix(matrix):
    if not matrix or not isinstance(matrix, list):
        raise Exception("Матрица пуста или не является списком")

    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
