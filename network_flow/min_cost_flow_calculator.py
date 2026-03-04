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
        max_iterations = self._order * self._order * 2
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            n = self._order

            distance_matrix = [[inf] * n for _ in range(n)]
            for from_node in range(n):
                distance_matrix[from_node][from_node] = 0
                for to_node in range(n):
                    if self._residual_matrix[from_node][to_node] > 0:
                        distance_matrix[from_node][to_node] = (
                            self._cost_residual_matrix[from_node][to_node]
                        )

            try:
                floyd_warshall(distance_matrix)
                break
            except NegativeLoopFloydWarshallError as e:
                loop = self._find_negative_loop(e.detected_vertex_idx)
                if loop and len(loop) >= 3:
                    self._remove_negative_loop(loop)
                else:
                    break
        self._set_flow_matrix_by_residual_matrix()

    def _find_negative_loop(self, start_vertex_idx) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети
        стоимости транспортировки"""
        n = self._order
        distance_matrix = [[inf] * n for _ in range(n)]

        for from_node in range(n):
            distance_matrix[from_node][from_node] = 0
            for to_node in range(n):
                if self._residual_matrix[from_node][to_node] > 0:
                    distance_matrix[from_node][to_node] = self._cost_residual_matrix[from_node][to_node]

        for offset in range(n):
            start_node = (start_vertex_idx + offset) % n
            try:
                bellman_ford(distance_matrix, start_node)
            except NegativeLoopBellmanFordError as e:
                if e.predecessors:
                    current_node = e.last_updated_vertex_idx

                    for _ in range(n):
                        current_node = e.predecessors[current_node]

                    cycle_start = current_node
                    loop = [cycle_start]
                    current_node = e.predecessors[cycle_start]
                    while current_node != cycle_start:
                        loop.append(current_node)
                        current_node = e.predecessors[current_node]

                    loop.append(cycle_start)
                    loop.reverse()
                    return loop

        return []

    def _remove_negative_loop(self, loop) -> None:
        """Удаляет цикл отрицательной стоимости в остаточных сетях потоков и стоимостей."""

        if len(loop) < 3:
            return

        min_capacity = inf
        for i in range(len(loop) - 1):
            from_node = loop[i]
            to_node = loop[i + 1]
            if 0 < self._residual_matrix[from_node][to_node] < min_capacity:
                min_capacity = self._residual_matrix[from_node][to_node]

        if min_capacity <= 0 or min_capacity == inf:
            return

        total_cost = sum(
            self._cost_residual_matrix[loop[i]][loop[i + 1]]
            for i in range(len(loop) - 1)
        )
        if total_cost >= 0:
            return

        for i in range(len(loop) - 1):
            from_node = loop[i]
            to_node = loop[i + 1]

            self._residual_matrix[from_node][to_node] -= min_capacity
            self._residual_matrix[to_node][from_node] += min_capacity

            edge_cost = self._cost_residual_matrix[from_node][to_node]
            if edge_cost != 0:
                if self._residual_matrix[to_node][from_node] > 0:
                    self._cost_residual_matrix[to_node][from_node] = -edge_cost
                if self._residual_matrix[from_node][to_node] == 0:
                    self._cost_residual_matrix[from_node][to_node] = 0

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
        for from_node in range(self._order):
            for to_node in range(self._order):
                total_cost += (
                    self._flow_matrix[from_node][to_node]
                    * self._cost_matrix[from_node][to_node]
                )
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
