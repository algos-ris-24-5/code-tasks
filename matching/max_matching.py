from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.error_message_enum import ErrorMessageEnum
from collections import deque

def get_tree(bipartite_graph, matching, order):
    levels = [-1] * order
    queue = deque()
    for current_left in range(order):
        if not matching.is_left_covered(current_left):
            levels[current_left] = 0
            queue.append(current_left)
    found = False
    while queue:
        current_left = queue.popleft()
        for neighbor_of_left in bipartite_graph.right_neighbors(current_left):
            matched_left = matching.get_left_match(neighbor_of_left)
            if matched_left != -1 and levels[matched_left] == -1:
                levels[matched_left] = levels[current_left] + 1
                queue.append(matched_left)
            elif matched_left == -1:
                found = True
                return levels, found
    return levels, found

def find_chain(bipartite_graph, matching, current_left, levels, visited):
    visited[current_left] = True
    for neighbor_of_left in bipartite_graph.right_neighbors(current_left):
        matched_left = matching.get_left_match(neighbor_of_left)
        if matched_left == -1:
            return [(current_left, neighbor_of_left)]
        elif not visited[matched_left] and levels[matched_left] == levels[current_left] + 1:
            path = find_chain(bipartite_graph, matching, matched_left, levels, visited)
            if path is not None:
                path.append((current_left, neighbor_of_left))
                return path
    return None

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
        levels, found = get_tree(bipartite_graph, matching, order)
        if not found:
            break
        for current_left in range(order):
            if not matching.is_left_covered(current_left):
                visited = [False] * order
                path = find_chain(bipartite_graph, matching, current_left, levels, visited)
                if path:
                    for left, right in reversed(path):
                        matched_left = matching.get_left_match(right)
                        if matched_left != -1:
                            matching.remove_edge(matched_left, right)
                        matching.add_edge(left, right)
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
