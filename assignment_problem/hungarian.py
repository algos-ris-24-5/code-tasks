from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching


def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Матрица смежности, где ``True`` означает включение ребра в паросочетание.
    :rtype: list[list[bool]]
    """
    _validate_matrix(matrix)

    order = len(matrix)
    matching = BipartiteGraphMatching(order)
    reduced_matrix = get_reduced_matrix(matrix)
       
    while not matching.is_perfect:
        bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
        augmented, visited_rows, visited_cols = _bfs_augment(bipartite_graph, matching)

        if not augmented:
            _diagonal_reduction(reduced_matrix, visited_rows, visited_cols)

    return matching

def _validate_matrix(matrix):
    if not matrix or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Передана некорректная матрица")
    
    order = len(matrix)
    for row in matrix:
        if len(row) != order:
            raise ValueError("Передана некорректная матрица")
        for value in row:
            if value is None or isinstance(value, (str, list)) or value < 0 or not isinstance(value, (int, float)):
                raise ValueError("Передана некорректная матрица")


def _bfs_augment(graph: BipartiteGraph, matching: BipartiteGraphMatching):
    order = graph.order
    parent = {}
    visited_rows = set()
    visited_cols = set()

    current_front_rows = []
    for row_index in range(order):
        if not matching.is_left_covered(row_index):
            current_front_rows.append(row_index)
            visited_rows.add(row_index)

    while current_front_rows:
        next_front_cols = []
        for row_index in current_front_rows:
            for col_index in graph.right_neighbors(row_index):
                if col_index not in visited_cols:
                    visited_cols.add(col_index)
                    parent[col_index] = row_index
                    next_front_cols.append(col_index)

                    if not matching.is_right_covered(col_index):
                        _apply_path(matching, parent, col_index)
                        return True, set(), set()

        current_front_rows = []
        for col_index in next_front_cols:
            matched_row = matching.get_left_match(col_index)
            if matched_row != -1 and matched_row not in visited_rows:
                visited_rows.add(matched_row)
                current_front_rows.append(matched_row)

    return False, visited_rows, visited_cols

def _apply_path(matching: BipartiteGraphMatching, parent: dict, last_col: int):
    current_col = last_col
    while current_col in parent:
        current_row = parent[current_col]
        if matching.is_left_covered(current_row):
            old_col = matching.get_right_match(current_row)
            matching.remove_edge(current_row, old_col)
        else:
            old_col = None
        matching.add_edge(current_row, current_col)
        current_col = old_col


def _diagonal_reduction(matrix: list[list[int | float]], visited_rows: set, visited_cols: set):
    order = len(matrix)
    delta = float('inf')

    for row_index in visited_rows:
        for col_index in range(order):
            if col_index not in visited_cols and matrix[row_index][col_index] < delta:
                delta = matrix[row_index][col_index]

    if delta == float('inf') or delta == 0:
        return

    for row_index in range(order):
        for col_index in range(order):
            if row_index in visited_rows:
                matrix[row_index][col_index] -= delta
            if col_index in visited_cols:
                matrix[row_index][col_index] += delta

def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    adjacency_lists = {}
    for row_idx in range(len(reduced_matrix)):
        adjacency_lists[row_idx] = [col_idx for col_idx, value in enumerate(reduced_matrix[row_idx]) if value == 0]
    return BipartiteGraph(adjacency_lists)


def get_reduced_matrix(matrix: list[list[int | float]]) -> list[list[int | float]]:
    """
    Выполняет редукцию матрицы, уменьшая значения в строках и столбцах.

    :param matrix: Исходная квадратная матрица весов.
    :type matrix: list[list[int|float]]
    :return: Редуцированная матрица, где минимальные значения в строках и столбцах равны 0.
    :rtype: list[list[int|float]]
    """
    reduced_matrix = [[val - min(row) for val in row] for row in matrix]

    for col_idx in range(len(reduced_matrix[0])):
        min_col_value = reduced_matrix[0][col_idx]
        for row_idx in range(1, len(reduced_matrix)):
            if reduced_matrix[row_idx][col_idx] < min_col_value:
                min_col_value = reduced_matrix[row_idx][col_idx]
        for row_idx in range(len(reduced_matrix)):
            reduced_matrix[row_idx][col_idx] -= min_col_value

    return reduced_matrix

if __name__ == "__main__":
    matrix = [
        [6, 7, 8, 14, 7],
        [8, 14, 6, 9, 7],
        [14, 14, 13, 9, 11],
        [5, 12, 10, 9, 14],
        [6, 10, 8, 10, 15],
    ]
    print("Исходная матрица")
    for row in matrix:
        print(row)
    print()

    reduced_matrix = get_reduced_matrix(matrix)
    print("Редуцированная матрица")
    for row in reduced_matrix:
        print(row)
    print()

    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    print("Двудольный граф")
    print(bipartite_graph)
    print()

    matching = hungarian(matrix)
    print("Совершенное паросочетание найденное венгерским алгоритмом")
    print(matching.get_matching())
