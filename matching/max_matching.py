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
    
    matching = BipartiteGraphMatching(bipartite_graph.order)
    
    while True:
        chain_result = _find_alternating_chain(bipartite_graph, matching)
        if chain_result is None:
            break
        
        chain_end_vertex, left_predecessor, right_predecessor = chain_result
        
        edges_to_remove = []
        edges_to_add = []
        
        current_right = chain_end_vertex
        while current_right is not None:
            current_left = right_predecessor[current_right]
            edges_to_add.append((current_left, current_right))
            
            if current_left in left_predecessor and left_predecessor[current_left] is not None:
                previous_right = left_predecessor[current_left]
                edges_to_remove.append((current_left, previous_right))
                current_right = previous_right
            else:
                current_right = None
        
        for left_vertex, right_vertex in edges_to_remove:
            matching.remove_edge(left_vertex, right_vertex)
        
        for left_vertex, right_vertex in edges_to_add:
            matching.add_edge(left_vertex, right_vertex)
    
    return matching


def _find_alternating_chain(bipartite_graph, matching):
    """
    Ищет чередующуюся цепь с помощью волнового метода.
    Возвращает кортеж (конечная_свободная_вершина, предшественники_левых, предшественники_правых)
    или None, если цепь не найдена.
    """
    wave_queue = deque()
    left_predecessor = {}
    right_predecessor = {}
    visited_left_vertices = set()
    visited_right_vertices = set()
    graph_order = bipartite_graph.order
    
    for left_vertex in range(graph_order):
        if not matching.is_left_covered(left_vertex):
            wave_queue.append(left_vertex)
            visited_left_vertices.add(left_vertex)
            left_predecessor[left_vertex] = None
    
    while wave_queue:
        current_left = wave_queue.popleft()
        
        for current_right in bipartite_graph.right_neighbors(current_left):
            if current_right in visited_right_vertices:
                continue
            
            visited_right_vertices.add(current_right)
            right_predecessor[current_right] = current_left
            
            if not matching.is_right_covered(current_right):
                return current_right, left_predecessor, right_predecessor
            
            next_left = matching.get_left_match(current_right)
            if next_left not in visited_left_vertices:
                visited_left_vertices.add(next_left)
                left_predecessor[next_left] = current_right
                wave_queue.append(next_left)
    
    return None


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
