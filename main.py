def validate_matrix(matrix: list[list[int]]) -> None:
    """Проверяет, что матрица является квадратной трехдиагональной.
    
    :param matrix: матрица для проверки
    :raise Exception: если матрица некорректна
    """
    if matrix is None:
        raise Exception("Матрица не может быть None")
        
    n = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise Exception(f"Матрица должна быть квадратной. Строка {i} имеет длину {len(row)}, ожидалось {n}")

    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and matrix[i][j] != 0:
                raise Exception(f"Матрица не является трехдиагональной. Элемент [{i}][{j}] = {matrix[i][j]} должен быть 0")


def create_submatrix_remove_first(matrix: list[list[int]], remove_count: int) -> list[list[int]]:
    """Создает подматрицу, удаляя первые remove_count строк и столбцов.
    
    :param matrix: исходная матрица
    :param remove_count: количество строк и столбцов для удаления с начала
    :return: подматрица
    """
    return [row[remove_count:] for row in matrix[remove_count:]]


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивно вычисляет определитель трехдиагональной матрицы.
    :param matrix: трехдиагональная квадратная матрица
    :return: значение определителя
    """
    n = len(matrix)
    
    if n == 0:
        return 1

    if n == 1:
        return matrix[0][0]
    
    a_1 = matrix[0][0] 
    b_1 = matrix[0][1] 
    c_1 = matrix[1][0] 
    
    submatrix_n_minus_1 = create_submatrix_remove_first(matrix, 1) 
    submatrix_n_minus_2 = create_submatrix_remove_first(matrix, 2) 
    
    det_n_minus_1 = calculate_determinant(submatrix_n_minus_1)
    det_n_minus_2 = calculate_determinant(submatrix_n_minus_2)
    
    return a_1 * det_n_minus_1 - b_1 * c_1 * det_n_minus_2


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.

    :param matrix: целочисленная трехдиагональная квадратная матрица.
    :return: значение определителя.
    :raise Exception: если матрица некорректна.
    """
    validate_matrix(matrix)
    return calculate_determinant(matrix)

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
