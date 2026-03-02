from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator
from shortest_path.bellman_ford import (
    NegativeLoopBellmanFordError,
    bellman_ford,
    restore_path,
)
from shortest_path.floyd_warshall import NegativeLoopFloydWarshallError, floyd_warshall

COST_MATRIX_NAME = "Таблица стоимости транспортировки"


class MinCostFlowCalculator(MaxFlowCalculator):
    """Класс для решения задачи поиска максимального потока минимальной стоимости"""

    def __init__(self, capacity_matrix: list[list[int]], cost_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        :param cost_matrix: Квадратная матрица стоимости транспортировки.
        :type cost_matrix: list[list[int]]
        """
        NetworkValidator.validate_matrix(cost_matrix, COST_MATRIX_NAME)
        # Максимальный поток рассчитывается в родительском классе,
        # сохраняется значением максимального потока и матрица локальных потоков
        super().__init__(capacity_matrix)

        self._cost_matrix = cost_matrix
        self._residual_matrix, self._cost_residual_matrix = (
            self._get_residual_matrices()
        )
        self._minimize_cost()
        self._min_cost = self._get_cost_by_flow()

    @property
    def min_cost(self) -> int:
        """Возвращает минимальную стоимость потока"""
        return self._min_cost

    def _minimize_cost(self) -> None:
        """Осуществляет минимизацию стоимости максимального потока
        посредством поиска и удаления отрицательных циклов в остаточной сети.
        После удаления всех циклов обновляет матрицу локальных потоков
        на основе остаточной сети."""
        while True:
            negative_loop = self._find_negative_loop(0)
            if not negative_loop:
                break
            self._remove_negative_loop(negative_loop)
            self._set_flow_matrix_by_residual_matrix()
            self._residual_matrix, self._cost_residual_matrix = self._get_residual_matrices()
        
        self._set_flow_matrix_by_residual_matrix()

    def _find_negative_loop(self, start_vertex_idx) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети
        стоимости транспортировки"""
        order = self._order
        
        distance_matrix = [[None] * order for _ in range(order)]
        
        for row_index in range(order):
            for col_index in range(order):
                if self._residual_matrix[row_index][col_index] > 0:
                    distance_matrix[row_index][col_index] = self._cost_residual_matrix[row_index][col_index]
        
        for vertex_index in range(order):
            try:
                bellman_ford(distance_matrix, vertex_index)
            except NegativeLoopBellmanFordError as error:
                predecessors = error.predecessors
                last_updated_vertex_idx = error.last_updated_vertex_idx
                
                cycle_vertex = last_updated_vertex_idx
                for _ in range(order):
                    if predecessors[cycle_vertex] is not None:
                        cycle_vertex = predecessors[cycle_vertex]
                
                negative_loop = [cycle_vertex]
                current_vertex = predecessors[cycle_vertex]
                while current_vertex != cycle_vertex and current_vertex is not None:
                    negative_loop.append(current_vertex)
                    current_vertex = predecessors[current_vertex]
                negative_loop.append(cycle_vertex)
                negative_loop.reverse()
                
                return negative_loop
        
        return []

    def _remove_negative_loop(self, loop) -> None:
        """Удаляет цикл отрицательной стоимости в остаточных сетях потоков и стоимостей."""
        if len(loop) < 2:
            return
        
        min_capacity = inf
        for edge_index in range(len(loop) - 1):
            source_vertex = loop[edge_index]
            target_vertex = loop[edge_index + 1]
            if self._residual_matrix[source_vertex][target_vertex] > 0:
                min_capacity = min(min_capacity, self._residual_matrix[source_vertex][target_vertex])
        
        if min_capacity == inf or min_capacity <= 0:
            return
        
        for edge_index in range(len(loop) - 1):
            source_vertex = loop[edge_index]
            target_vertex = loop[edge_index + 1]
            self._residual_matrix[source_vertex][target_vertex] -= min_capacity
            self._residual_matrix[target_vertex][source_vertex] += min_capacity

    def _get_residual_matrices(self):
        """Возвращает остаточные сети, созданные на основе матриц
        локальных потоков и пропускных способностей:
        - residual_matrix - остаточная сеть с указанием потоков и резервов.
        - cost_residual_matrix - остаточная сеть с указанием стоимости транспортировки.
        """
        residual_matrix = [[0] * self._order for _ in range(self._order)]
        cost_residual_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                flow = self._flow_matrix[row_idx][col_idx]
                reserve = (
                    self._capacity_matrix[row_idx][col_idx]
                    - self._flow_matrix[row_idx][col_idx]
                )
                cost = self._cost_matrix[row_idx][col_idx]
                if flow:
                    residual_matrix[row_idx][col_idx] = flow
                    cost_residual_matrix[row_idx][col_idx] = -cost
                if reserve:
                    residual_matrix[col_idx][row_idx] = reserve
                    cost_residual_matrix[col_idx][row_idx] = cost

        return residual_matrix, cost_residual_matrix

    def _get_cost_by_flow(self) -> int:
        """Возвращает суммарную стоимость транспортировки на основе матрицы локальных потоков
        и матрицы стоимостей"""
        total_cost = 0
        for row_index in range(self._order):
            for col_index in range(self._order):
                if self._flow_matrix[row_index][col_index] > 0:
                    total_cost += self._flow_matrix[row_index][col_index] * self._cost_matrix[row_index][col_index]
        return total_cost


if __name__ == "__main__":
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    cost_matrix = [
        # s a  b  c  d  t
        [0, 3, 2, 4, 0, 0],  # s
        [0, 0, 0, 4, 5, 0],  # a
        [0, 2, 0, 2, 0, 0],  # b
        [0, 0, 0, 0, 2, 0],  # c
        [0, 0, 0, 0, 0, 1],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока минимальной стоимости:")
    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    print("Величина максимального потока:", calculator._max_flow)
    print("Стоимость потока:", calculator._min_cost)
    print("Матрица локальных потоков")
    for row in calculator._flow_matrix:
        print(row)
