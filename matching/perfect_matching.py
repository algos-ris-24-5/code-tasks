from collections import deque
from matching.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching
from matching.errors.perfect_matching_error import PerfectMatchingError


def find_augmenting_path(
    bipartite_graph: BipartiteGraph,
    matching: BipartiteGraphMatching,
    tree_root: int,
):
    """
    Алгоритм последовательно ищет увеличивающие (чередующиеся) пути относительно текущего
    паросочетания, начиная с пустого.

    :param bipartite_graph: Двудольный граф, заданный списками смежности левой доли.
    :param matching: Список обнаруженных паросочетаний в заданном двудольном графе.
    :param matching: Корень чередующейся цепи.
    """
    queue_left_part = deque()
    history_to_restore_path_right_part = [-1] * matching.order
    visited_right_part = [False] * matching.order

    last_vertex_alternating_chain = -1
    flag_exit_to_main_cycle = False

    queue_left_part.append(tree_root)

    while len(queue_left_part) != 0:
        current_index_left = queue_left_part.popleft()

        for current_index_right in bipartite_graph.right_neighbors(current_index_left):
            if not visited_right_part[current_index_right]:
                visited_right_part[current_index_right] = True
                history_to_restore_path_right_part[current_index_right] = current_index_left

                if matching.is_right_covered(current_index_right):
                    next_index_left = matching.get_left_match(current_index_right)
                    queue_left_part.append(next_index_left)
                else:
                    last_vertex_alternating_chain = current_index_right
                    flag_exit_to_main_cycle = True
                    break

        if flag_exit_to_main_cycle:
            break

    if flag_exit_to_main_cycle:
        return last_vertex_alternating_chain, history_to_restore_path_right_part

    return None, history_to_restore_path_right_part


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

    while not matching.is_perfect:
        tree_root = -1
        for i in range(matching.order):
            if not matching.is_left_covered(i):
                tree_root = i
                break

        last_vertex_alternating_chain, history_to_restore_path_right_part = (
            find_augmenting_path(bipartite_graph, matching, tree_root)
        )

        if last_vertex_alternating_chain is None:
            raise PerfectMatchingError(ErrorMessageEnum.NOT_EXISTED_PERFECT_MATCH)

        current_vertex_right = last_vertex_alternating_chain

        while current_vertex_right != -1:
            current_vertex_left = history_to_restore_path_right_part[current_vertex_right]

            next_step_right = -1
            if matching.is_left_covered(current_vertex_left):
                next_step_right = matching.get_right_match(current_vertex_left)
                matching.remove_edge(current_vertex_left, next_step_right)

            matching.add_edge(current_vertex_left, current_vertex_right)
            current_vertex_right = next_step_right

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
    print(get_perfect_matching(bipartite_graph))
