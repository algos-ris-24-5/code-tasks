def validate_matrix(matrix: list[list[int]]) -> None:
    """Проверяет, что матрица является квадратной трехдиагональной.
    
    :param matrix: матрица для проверки
    :raise Exception: если матрица некорректна
    """
    if matrix is None:
        raise Exception("Матрица не может быть None")
        
    n = len(matrix)
    if n == 0:
        raise Exception("Матрица не может быть пустой")

    for i, row in enumerate(matrix):
        if len(row) != n:
            raise Exception(f"Матрица должна быть квадратной. Строка {i} имеет длину {len(row)}, ожидалось {n}")

    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and matrix[i][j] != 0:
                raise Exception(f"Матрица не является трехдиагональной. Элемент [{i}][{j}] = {matrix[i][j]} должен быть 0")

    if n >= 1:
        main_val = matrix[0][0]
        for i in range(1, n):
            if matrix[i][i] != main_val:
                raise Exception(f"Главная диагональ не постоянна: элемент [{i}][{i}] = {matrix[i][i]}, ожидалось {main_val}")

    if n >= 2:
        upper_val = matrix[0][1]
        for i in range(n - 1):
            if matrix[i][i + 1] != upper_val:
                raise Exception(f"Верхняя диагональ не постоянна: элемент [{i}][{i+1}] = {matrix[i][i+1]}, ожидалось {upper_val}")

        lower_val = matrix[1][0]
        for i in range(1, n):
            if matrix[i][i - 1] != lower_val:
                raise Exception(f"Нижняя диагональ не постоянна: элемент [{i}][{i-1}] = {matrix[i][i-1]}, ожидалось {lower_val}")


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
    
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    
    sub1 = create_submatrix_remove_first(matrix, 1)
    sub2 = create_submatrix_remove_first(matrix, 2)
    
    return a * calculate_determinant(sub1) - b * c * calculate_determinant(sub2)


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
