from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from collections import deque

from matching.errors.perfect_matching_error import PerfectMatchingError


def get_perfect_matching(bipartite_graph: BipartiteGraph) -> BipartiteGraphMatching:
    """
    Находит совершенное паросочетание в двудольном графе с долями равной мощности.

    Алгоритм последовательно ищет увеличивающие (чередующиеся) пути относительно текущего
    паросочетания, начиная с пустого. Каждый найденный путь используется для увеличения
    мощности паросочетания на единицу. Процесс продолжается, пока существуют непокрытые
    вершины в левой доле и найдены увеличивающие пути.

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :return: Объект BipartiteGraphMatching, представляющий совершенное паросочетание.
    :raises PerfectMatchingError: Если совершенное паросочетание не существует в данном графе.
    """
    if not isinstance(bipartite_graph, BipartiteGraph):
        raise TypeError(ErrorMessageEnum.WRONG_GRAPH)

    node_count = bipartite_graph.order
    result_matching = BipartiteGraphMatching(node_count)

    for left_node_idx in range(node_count):
        
        if result_matching.is_left_covered(left_node_idx):
            continue

        success = _try_build_chain(left_node_idx, bipartite_graph, result_matching)

        if not success:
            raise PerfectMatchingError("Совершенное паросочетание не найдено")

    if result_matching.cardinality != node_count:
        raise PerfectMatchingError(ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)

    return result_matching


def _try_build_chain(start_node: int, graph: BipartiteGraph, matching: BipartiteGraphMatching) -> bool:

    order = graph.order
    links_to_parents = [-1] * order
    queue = deque([start_node])
    target_right_node = -1

    while queue:
        current_left = queue.popleft()
        neighbors = graph.right_neighbors(current_left)
        
        for right_candidate in neighbors:
            if links_to_parents[right_candidate] != -1:
                continue
            
            links_to_parents[right_candidate] = current_left
            
            if not matching.is_right_covered(right_candidate):
                target_right_node = right_candidate
                break

            else:
                next_left = matching.get_left_match(right_candidate)
                queue.append(next_left)
        
        if target_right_node != -1:
            break
    
    if target_right_node != -1:
        _apply_inversion(target_right_node, links_to_parents, matching)
        return True
        
    return False


def _apply_inversion(end_node: int, links: list, matching: BipartiteGraphMatching) -> None:

    current_right = end_node
    
    while True:
        parent_left = links[current_right]
        
        if matching.is_left_covered(parent_left):
            prev_match_right = matching.get_right_match(parent_left)
            matching.remove_edge(parent_left, prev_match_right)
            matching.add_edge(parent_left, current_right)
            current_right = prev_match_right
        
        else:
            matching.add_edge(parent_left, current_right)
            break


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
    print(get_perfect_matching(bipartite_graph))