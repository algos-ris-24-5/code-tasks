def validate_matrix(matrix: list[list[int]]) -> None:
    """Проверяет, является ли матрица целочисленной квадратной матрицей
    :param matrix: матрица для проверки
    :raise Exception: если значение параметра не является целочисленной квадратной матрицей
    """

    if not matrix or not isinstance(matrix, list):
        raise Exception("Матрица должна быть непустым списком")

    if not all(isinstance(row, list) for row in matrix):
        raise Exception("Матрица должна быть списком списков")
    
    n = len(matrix)
    if n == 0:
        raise Exception("Матрица не может быть пустой")
    

    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")
    

    for row in matrix:
        if not all(isinstance(item, int) for item in row):
            raise Exception("Все элементы матрицы должны быть целыми числами")


def calculate_determinant_recursive(matrix: list[list[int]]) -> int:
    """Рекурсивно вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :return: значение определителя
    """
    n = len(matrix)
    
    if n == 1:
        return matrix[0][0]
    
    det = 0
    for idx, item in enumerate(matrix[0]):
        reduced_matrix = get_reduced_matrix(matrix, 0, idx)
        det += item * (-1) ** idx * calculate_determinant_recursive(reduced_matrix)
    return det


def get_reduced_matrix(matrix: list[list[int]], row_idx: int, col_idx: int) -> list[list[int]]:
    """Возвращает матрицу без указанной строки и столбца
    
    :param matrix: исходная матрица
    :param row_idx: индекс строки для исключения
    :param col_idx: индекс столбца для исключения
    :return: редуцированная матрица
    """
    return [
        [row[j] for j in range(len(row)) if j != col_idx]
        for i, row in enumerate(matrix) if i != row_idx
    ]


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной квадратной матрицей
    :return: значение определителя
    """
    validate_matrix(matrix)
    return calculate_determinant_recursive(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()