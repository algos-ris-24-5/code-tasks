from collections import namedtuple


INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])


def validate_price_table(price_table: list[list[float | int]]) -> None:

    if not price_table:
        raise ValueError(PARAM_ERR_MSG)
    
    if len(price_table[0]) == 0:
        raise ValueError(PARAM_ERR_MSG)

    row_lengths = [len(row) for row in price_table]
    if not all(length == row_lengths[0] for length in row_lengths):
        raise ValueError(PARAM_ERR_MSG)

    for i, row in enumerate(price_table):
        for j, value in enumerate(row):
            if not isinstance(value, (int, float)):
                raise ValueError(PARAM_ERR_MSG)


def initialize_dp_tables(rows: int, cols: int) -> tuple:
    cost_dp = [[0] * cols for _ in range(rows)]
    path_dp = [[None] * cols for _ in range(rows)]
    return cost_dp, path_dp


def fill_first_row_and_column(cost_dp: list[list], path_dp: list[list], 
                               price_table: list[list], rows: int, cols: int) -> None:

    cost_dp[0][0] = price_table[0][0]
    path_dp[0][0] = (-1, -1)
    

    for j in range(1, cols):
        cost_dp[0][j] = cost_dp[0][j-1] + price_table[0][j]
        path_dp[0][j] = (0, j-1)
    

    for i in range(1, rows):
        cost_dp[i][0] = cost_dp[i-1][0] + price_table[i][0]
        path_dp[i][0] = (i-1, 0)


def fill_remaining_cells(cost_dp: list[list], path_dp: list[list], 
                          price_table: list[list], rows: int, cols: int) -> None:
    for i in range(1, rows):
        for j in range(1, cols):
            from_top = cost_dp[i-1][j]
            from_left = cost_dp[i][j-1]
            
            if from_top <= from_left:
                cost_dp[i][j] = from_top + price_table[i][j]
                path_dp[i][j] = (i-1, j)
            else:
                cost_dp[i][j] = from_left + price_table[i][j]
                path_dp[i][j] = (i, j-1)


def reconstruct_path(path_dp: list[list], rows: int, cols: int) -> list:
    path = []
    i, j = rows - 1, cols - 1
    
    path.append((i, j))
    
    while (i, j) != (0, 0):
        i, j = path_dp[i][j]
        path.append((i, j))
    
    path.reverse()
    return path


def get_min_cost_path(
    price_table: list[list[float | int]],
) -> Result:
    """Возвращает путь минимальной стоимости в таблице из левого верхнего угла
    в правый нижний. Каждая ячейка в таблице имеет цену посещения. Перемещение
    из ячейки в ячейку можно производить только по горизонтали вправо или по
    вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    :return: Именованный кортеж Result с полями:
    cost - стоимость минимального пути,
    path - путь, список кортежей с индексами ячеек.
    """
    validate_price_table(price_table)
    
    rows = len(price_table)
    cols = len(price_table[0]) if rows > 0 else 0
    
    cost_dp, path_dp = initialize_dp_tables(rows, cols)

    fill_first_row_and_column(cost_dp, path_dp, price_table, rows, cols)
    
    fill_remaining_cells(cost_dp, path_dp, price_table, rows, cols)
    
    path = reconstruct_path(path_dp, rows, cols)
    
    return Result(cost=cost_dp[rows-1][cols-1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()