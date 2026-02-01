from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum
from collections import deque


def get_max_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит максимальное по мощности паросочетание в двудольном графе с долями равной мощности.

    Алгоритм начинает с пустого паросочетания и последовательно ищет увеличивающие 
    (чередующиеся) пути относительно текущего паросочетания. Каждый найденный путь 
    используется для увеличения мощности паросочетания на единицу. Процесс завершается, 
    когда увеличивающих путей больше не существует — в этот момент паросочетание 
    становится максимальным (по теореме Бержа).

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий максимальное паросочетание.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)
    order = bipartite_graph.order
    matching = BipartiteGraphMatching(order)

    while True:
        parent_left = [-1] * order 
        parent_right = [-1] * order 
        visited_left = [False] * order
        visited_right = [False] * order
        queue = deque()
        for u in range(order):
            if not matching.is_left_covered(u):
                queue.append(('L', u))
                visited_left[u] = True
        found_path = False
        end_right = -1

        while queue and not found_path:
            side, vertex = queue.popleft()

            if side == 'L':
                for v in bipartite_graph.right_neighbors(vertex):
                    if not visited_right[v]:
                        visited_right[v] = True
                        parent_right[v] = vertex
                        queue.append(('R', v))
            else: 
                if not matching.is_right_covered(vertex):
                    end_right = vertex
                    found_path = True
                    break
                else:
                    matched_left = matching.get_left_match(vertex)
                    if not visited_left[matched_left]:
                        visited_left[matched_left] = True
                        parent_left[matched_left] = vertex
                        queue.append(('L', matched_left))

        if not found_path:
            break 
        current_right = end_right
        while current_right != -1:
            u = parent_right[current_right]
            old_v = matching.get_right_match(u)
            if old_v != -1:
                matching.remove_edge(u, old_v)
            matching.add_edge(u, current_right)
            if parent_left[u] == -1:
                break
            current_right = parent_left[u]
    return matching


if __name__ == "__main__":
    print("Исходный двудольный граф")
    bipartite_graph = BipartiteGraph({
        0: [0, 1],
        1: [0, 4],
        2: [1, 2, 3],
        3: [1, 2, 4],
        4: [0, 4],
    })
    print(bipartite_graph)

    print("Полученное паросочетание")
    print(get_max_matching(bipartite_graph))
