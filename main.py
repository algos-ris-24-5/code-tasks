def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    if not matrix or not isinstance(matrix,list):
        raise Exception("matrix is empty")
    
    for i in matrix:
        if len(i)!=len(matrix):
            raise Exception("matrix is not square")
            
    if len(matrix)==1:
        return matrix[0][0]
    
    det = 0
    
    for idx,item in enumerate(matrix[0]):
        reduced_matrix = _get_reduced_matrix(matrix,0,idx)
        det+= item * (-1) ** idx * calculate_determinant(reduced_matrix)
    return det

def _get_reduced_matrix(matrix, zero, idx):
    new_matrix = [row[:] for row in matrix]
    new_matrix.pop(zero)
    for i in range(len(new_matrix)):
        new_matrix[i].pop(idx)
    return new_matrix

def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
