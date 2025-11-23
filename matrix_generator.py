import random
from collections import namedtuple

Case = namedtuple("Case", ["matrix", "det"])
MAX_RANDOM_VALUE = 10
MIN_RANDOM_VALUE = 1


def generate_matrix_and_det(order) -> Case:
    """Генерирует случайную квадратную целочисленную матрицу с заранее
    известным значением определителя.

    :param order: порядок матрицы
    :raise Exception: если порядок матрицы не является целым числом или
                      меньше 1
    :return: именованный кортеж Case с полями matrix, det
    """
    if not isinstance(order, int) or order < 1:
        raise Exception("Порядок матрицы должен быть целым числом >= 1")

    matrix = [[0 for _ in range(order)] for _ in range(order)]

    det = 1
    for i in range(order):
        if random.random() < 0.5:
            diag_value = 1
        else:
            diag_value = random.randint(MIN_RANDOM_VALUE, MAX_RANDOM_VALUE)

        det *= diag_value

        for j in range(order):
            if j < i:
                matrix[i][j] = random.randint(MIN_RANDOM_VALUE, MAX_RANDOM_VALUE)
            elif j == i:
                matrix[i][j] = diag_value
            else:
                matrix[i][j] = 0
  
    num_operations = order * 4

    for _ in range(num_operations):
        op_type = random.choice(["row_add", "col_add", "row_swap", "col_swap"])

        if op_type == "row_add":
            i = random.randrange(order)
            j = random.randrange(order)
            if i != j:
                k = random.randint(-3, 3)
                if k != 0:
                    for col in range(order):
                        matrix[i][col] += k * matrix[j][col]

        elif op_type == "col_add":
            i = random.randrange(order)
            j = random.randrange(order)
            if i != j:
                k = random.randint(-3, 3)
                if k != 0:
                    for row in range(order):
                        matrix[row][i] += k * matrix[row][j]

        elif op_type == "row_swap":
            i = random.randrange(order)
            j = random.randrange(order)
            if i != j:
                matrix[i], matrix[j] = matrix[j], matrix[i]
                det = -det

        elif op_type == "col_swap":
            i = random.randrange(order)
            j = random.randrange(order)
            if i != j:
                for row in range(order):
                    matrix[row][i], matrix[row][j] = matrix[row][j], matrix[row][i]
                det = -det

    return Case(matrix=matrix, det=det)


def main():
    n = 10
    print(f"Генерация матрицы порядка {n}")
    result = generate_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result.det)
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in result.matrix]))


if __name__ == "__main__":
    main()
