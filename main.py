from collections import namedtuple


INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])


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
    if not isinstance(price_table, list) or not price_table:
        raise ValueError(PARAM_ERR_MSG)

    if any(not isinstance(row, list) or not row for row in price_table):
        raise ValueError(PARAM_ERR_MSG)

    rows = len(price_table)
    cols = len(price_table[0])

    for row in price_table:
        if len(row) != cols:
            raise ValueError(PARAM_ERR_MSG)
        for cell in row:
            if cell is not None and not isinstance(cell, (int, float)):
                raise ValueError(PARAM_ERR_MSG)

    dp = [[INF] * (cols + 1) for _ in range(rows + 1)]
    parent = [[None] * (cols + 1) for _ in range(rows + 1)]

    if price_table[0][0] is not None:
        dp[1][1] = price_table[0][0]

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if price_table[i-1][j-1] is not None:
                value = price_table[i-1][j-1]
                min_prev = min(dp[i-1][j], dp[i][j-1])
                if min_prev != INF:
                    dp[i][j] = min_prev + value
                    if dp[i-1][j] <= dp[i][j-1]:
                        parent[i][j] = (i-1, j)
                    else:
                        parent[i][j] = (i, j-1)

    if dp[rows][cols] == INF:
        return Result(cost=None, path=None)

    path = []
    i, j = rows, cols
    while i > 0 and j > 0:
        path.append((i-1, j-1))
        if i == 1 and j == 1:
            break
        i, j = parent[i][j]

    path.reverse()

    return Result(dp[rows][cols], path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
