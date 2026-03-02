from collections import namedtuple
from assignment_problem.errors.error_message_enum import ErrorMessageEnum
from matching.bipartite_graph_matching import BipartiteGraphMatching
from network_flow.min_cost_flow_calculator import MinCostFlowCalculator


AssignmentSolution = namedtuple("AssignmentSolution", ["cost", "assignments"])

def get_assignments(cost_matrix: list[list[int | float]]) -> AssignmentSolution:
    """
    Решает задачу о назначениях с использованиемалгоритма поиска 
    максимального потока минимальной стоимости.

    Задача заключается в нахождении совершенного паросочетания "исполнителей" (строки)
    и "задач" (столбцы), минимизирующей суммарную стоимость выполнения.
    Предполагается, что входная матрица квадратная (число исполнителей равно числу задач).

    :param cost_matrix: Квадратная матрица стоимостей размера n×n,
                        где cost_matrix[i][j] — стоимость назначения i-го исполнителя на j-ю задачу.
    :return: Объект AssignmentSolution, содержащий минимальную суммарную стоимость
             и список пар (i, j), представляющих оптимальные назначения.
    :raises ValueError: Если матрица некорректна (неквадратная, пустая, содержит недопустимые значения).
    """
    _validate_matrix(cost_matrix)
    matching = get_min_cost_perfect_matching(cost_matrix)
    total_cost = 0
    assignments = matching.get_matching()
    for row_idx, col_idx in assignments:
        total_cost += cost_matrix[row_idx][col_idx]

    return AssignmentSolution(total_cost, assignments)



def get_min_cost_perfect_matching(assignment_matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Возвращает совершенное паросочетание с минимальной стоимостью, найденное с использованием алгоритма поиска 
    максимального потока минимальной стоимости.

    :param assignment_matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type assignment_matrix: list[list[int|float]]
    :return: Совершенное паросочетание с минимальной стоимостью.
    :rtype: BipartiteGraphMatching
    """
    matrix_size = len(assignment_matrix)
    
    total_vertices = 2 * matrix_size + 2
    source_vertex = 0
    sink_vertex = 2 * matrix_size + 1
    
    capacity_matrix: list[list[int]] = [[0] * total_vertices for _ in range(total_vertices)]
    cost_matrix: list[list[int]] = [[0] * total_vertices for _ in range(total_vertices)]
    
    for executor_index in range(matrix_size):
        capacity_matrix[source_vertex][executor_index + 1] = 1
        cost_matrix[source_vertex][executor_index + 1] = 0
    
    for executor_index in range(matrix_size):
        for task_index in range(matrix_size):
            capacity_matrix[executor_index + 1][matrix_size + 1 + task_index] = 1
            cost_matrix[executor_index + 1][matrix_size + 1 + task_index] = int(assignment_matrix[executor_index][task_index] * 1000)
    
    for task_index in range(matrix_size):
        capacity_matrix[matrix_size + 1 + task_index][sink_vertex] = 1
        cost_matrix[matrix_size + 1 + task_index][sink_vertex] = 0

    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    flow_matrix = calculator.flow_matrix
    matching = BipartiteGraphMatching(len(assignment_matrix))
    
    for executor_index in range(matrix_size):
        for task_index in range(matrix_size):
            if flow_matrix[executor_index + 1][matrix_size + 1 + task_index] > 0:
                matching.add_edge(executor_index, task_index)

    return matching

def _validate_matrix(matrix: list[list[int | float]]) -> None:
    if (
        not matrix
        or not isinstance(matrix, list)
        or not matrix[0]
        or not isinstance(matrix[0], list)
    ):
        raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
    row_cnt = len(matrix[0])
    for row in matrix:
        if len(row) != row_cnt:
            raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(ErrorMessageEnum.WRONG_MATRIX)


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

    matching = get_min_cost_perfect_matching(matrix)
    
    result = get_assignments(matrix)
    print("\nРешение задачи о назначениях")
    print(f"Стоимость назначения: {result.cost}")
    print("Назначения: ")
    for assignment in result.assignments:
        print(assignment)
