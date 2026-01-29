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
    
    matching = BipartiteGraphMatching(bipartite_graph.order)

    for left_vertex in range(bipartite_graph.order):
        if matching.is_left_covered(left_vertex):
            continue
            
        if not _bfs_augmenting_path(bipartite_graph, matching, left_vertex):
            raise PerfectMatchingError(ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)
    
    return matching

def _bfs_augmenting_path(graph: BipartiteGraph, matching: BipartiteGraphMatching, start_left: int) -> bool:
    order = graph.order
    visited_left = [False] * order
    visited_right = [False] * order
    parent_left = [-1] * order
    parent_right = [-1] * order
    
    queue = deque()
    queue.append(start_left)
    visited_left[start_left] = True
    
    while queue:
        current_left = queue.popleft()
        
        for right_neighbor in graph.right_neighbors(current_left):
            if visited_right[right_neighbor]:
                continue
                
            visited_right[right_neighbor] = True
            
            if not matching.is_right_covered(right_neighbor):
                _augment_matching(matching, current_left, right_neighbor, 
                                parent_left, parent_right)
                return True
            else:
                matched_left = matching.get_left_match(right_neighbor)
                if not visited_left[matched_left]:
                    visited_left[matched_left] = True
                    parent_left[matched_left] = current_left
                    parent_right[matched_left] = right_neighbor
                    queue.append(matched_left)
    
    return False


def _augment_matching(matching: BipartiteGraphMatching, start_left: int, end_right: int,
                     parent_left: list, parent_right: list) -> None:
    current_left = start_left
    current_right = end_right
    
    while True:
        matching.add_edge(current_left, current_right)
        
        if parent_left[current_left] == -1:
            break
            
        prev_right = parent_right[current_left]
        prev_left = parent_left[current_left]
        
        matching.remove_edge(prev_left, prev_right)
        
        current_left = prev_left
        current_right = prev_right





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
