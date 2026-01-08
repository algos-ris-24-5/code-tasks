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
    rows, cols = _validate_table(price_table)

    min_cost = [[INF] * (cols + 1) for _ in range(rows + 1)]
    prev_cell = [[None] * (cols + 1) for _ in range(rows + 1)]

    if price_table[0][0] is not None:
        min_cost[1][1] = price_table[0][0]

    for row_idx in range(1, rows + 1):
        for col_idx in range(1, cols + 1):
            cell_price = price_table[row_idx - 1][col_idx - 1]
            if cell_price is not None:
                min_prev = min(min_cost[row_idx - 1][col_idx], min_cost[row_idx][col_idx - 1])
                if min_prev != INF:
                    min_cost[row_idx][col_idx] = min_prev + cell_price
                    if min_cost[row_idx - 1][col_idx] <= min_cost[row_idx][col_idx - 1]:
                        prev_cell[row_idx][col_idx] = (row_idx - 1, col_idx)
                    else:
                        prev_cell[row_idx][col_idx] = (row_idx, col_idx - 1)

    if min_cost[rows][cols] == INF:
        return Result(cost=None, path=None)

    path = _build_path(prev_cell, rows, cols)
    return Result(min_cost[rows][cols], path)

def _build_path(prev_cells, rows, cols):
    if prev_cells[rows][cols] is None:
        return None

    path = []
    row_idx, col_idx = rows, cols
    while row_idx > 0 and col_idx > 0:
        path.append((row_idx - 1, col_idx - 1))
        if row_idx == 1 and col_idx == 1:
            break
        row_idx, col_idx = prev_cells[row_idx][col_idx]

    path.reverse()
    return path

def _validate_table(price_table):
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

    return rows, cols

def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
