from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum as MatchingErrorMessageEnum

def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Матрица смежности, где ``True`` означает включение ребра в паросочетание.
    :rtype: list[list[bool]]
    """
    if not matrix or not matrix[0]:
        return BipartiteGraphMatching(0)

    order = len(matrix)
    if any(len(row) != order for row in matrix):
        raise ValueError("Матрица должна быть квадратной")

    reduced_matrix = get_reduced_matrix(matrix)
    matching = BipartiteGraphMatching(order)

    _build_perfect_matching(reduced_matrix, matching)

    return matching

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


def _build_perfect_matching(reduced_matrix: list[list[int | float]], matching: BipartiteGraphMatching) -> None:
    order = matching.order
    if order == 0:
        return

    while not matching.is_perfect:
        root = _find_free_left_vertex(matching)
        if root is None:
            break

        while True:
            bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
            found, free_right, left_visited, right_visited, parent_right = _find_augmenting_path(
                bipartite_graph, matching, root
            )

            
            if found:
                _augment_matching(matching, parent_right, free_right)
                break
            
            delta = _min_uncovered_value(reduced_matrix, left_visited, right_visited)
            if delta == float("inf"):
                raise ValueError(MatchingErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)
            _adjust_matrix(reduced_matrix, left_visited, right_visited, delta)

    if not matching.is_perfect:
        raise ValueError(MatchingErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)


def _find_free_left_vertex(matching: BipartiteGraphMatching) -> int | None:
    for idx in range(matching.order):
        if not matching.is_left_covered(idx):
            return idx
    return None


def _find_augmenting_path(bipartite_graph: BipartiteGraph, matching: BipartiteGraphMatching, root: int) -> tuple[bool, int | None, list[bool], list[bool], list[int]]:
    order = matching.order
    left_visited = [False] * order
    right_visited = [False] * order
    parent_right = [-1] * order

    queue = deque([root])
    left_visited[root] = True

    while queue:
        left_vertex = queue.popleft()
        for right_vertex in bipartite_graph.right_neighbors(left_vertex):
            if right_visited[right_vertex]:
                continue
            right_visited[right_vertex] = True
            parent_right[right_vertex] = left_vertex
            matched_left = matching.get_left_match(right_vertex)
            if matched_left == -1:
                return True, right_vertex, left_visited, right_visited, parent_right
            if not left_visited[matched_left]:
                left_visited[matched_left] = True
                queue.append(matched_left)

    return False, None, left_visited, right_visited, parent_right


def _augment_matching(matching: BipartiteGraphMatching, parent_right: list[int], free_right: int | None) -> None:
    if free_right is None:
        return

    right_vertex = free_right
    while right_vertex != -1:
        left_vertex = parent_right[right_vertex]
        previous_right = matching.get_right_match(left_vertex)
        if previous_right != -1:
            matching.remove_edge(left_vertex, previous_right)
        matching.add_edge(left_vertex, right_vertex)
        right_vertex = previous_right


def _min_uncovered_value(reduced_matrix: list[list[int | float]], left_visited: list[bool], right_visited: list[bool]) -> float:
    order = len(reduced_matrix)
    min_value = float("inf")

    for row_idx in range(order):
        if not left_visited[row_idx]:
            continue
        row = reduced_matrix[row_idx]
        for col_idx in range(order):
            if right_visited[col_idx]:
                continue
            if row[col_idx] < min_value:
                min_value = row[col_idx]
    return min_value


def _adjust_matrix(reduced_matrix: list[list[int | float]], left_visited: list[bool], right_visited: list[bool], delta: float) -> None:
    order = len(reduced_matrix)

    for row_idx in range(order):
        if left_visited[row_idx]:
            row = reduced_matrix[row_idx]
            for col_idx in range(order):
                row[col_idx] -= delta
    for col_idx in range(order):
        if right_visited[col_idx]:
            for row_idx in range(order):
                reduced_matrix[row_idx][col_idx] += delta

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
