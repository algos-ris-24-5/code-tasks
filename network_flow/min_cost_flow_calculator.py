from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator
from shortest_path.bellman_ford import (
    NegativeLoopBellmanFordError,
    bellman_ford,
    restore_path,
)
from shortest_path.floyd_warshall import NegativeLoopFloydWarshallError, floyd_warshall, get_shortest_path

COST_MATRIX_NAME = "Таблица стоимости транспортировки"

class NegativeLoopNotFoundError(Exception):
    def __init__(self):
        super().__init__("Граф не содержит отрицательных циклов")


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
            try:
                negative_loop = self._find_negative_loop(0)
                self._remove_negative_loop(negative_loop)
            except NegativeLoopNotFoundError as e:
                break
        
        self._min_cost = self._get_cost_by_flow()


    def _find_negative_loop(self, start_vertex_idx) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети
        стоимости транспортировки"""
        try:
            matrix, parents_matrix = bellman_ford(self._cost_residual_matrix, start_vertex_idx)
            raise NegativeLoopNotFoundError()
        except NegativeLoopBellmanFordError as e:
            parents_matrix = e.predecessors
            v = e.last_updated_vertex_idx
            current = v
            for _ in range(self._order):
                if current is None:
                    raise NegativeLoopNotFoundError()
                current = parents_matrix[current]
            start_node = current
            negative_loop = [current]
            next_node = parents_matrix[current]
            while start_node != next_node:
                negative_loop.append(next_node)
                next_node = parents_matrix[next_node]
            negative_loop.append(current)
            negative_loop.reverse()
        return negative_loop

    def _remove_negative_loop(self, loop) -> None:
        """Удаляет цикл отрицательной стоимости в остаточных сетях потоков и стоимостей."""
        min_capacity = inf
        for i in range(len(loop) - 1):
            min_capacity = min(min_capacity, self._residual_matrix[loop[i]][loop[i + 1]])
        
        for i in range(len(loop) - 1):
            
            current = loop[i]
            next = loop[i + 1]
            
            if self._residual_matrix[next][current] == 0:
                self._cost_residual_matrix[next][current] = -self._cost_residual_matrix[current][next]
            
            self._residual_matrix[current][next] -= min_capacity
            self._residual_matrix[next][current] += min_capacity
            
            if self._residual_matrix[current][next] == 0:
                self._cost_residual_matrix[current][next] = 0
            
            if self._capacity_matrix[current][next] > 0:
                self._flow_matrix[current][next] -= min_capacity
            else:
                self._flow_matrix[next][current] += min_capacity

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
        cost = 0
        for i in range(self._order):
            for j in range(self._order):
                cost += self._flow_matrix[i][j] * self._cost_matrix[i][j]
        return cost

if __name__ == "__main__":
    capacity_matrix = [
            # s a  b  t
            [0, 2, 1, 0],  # s
            [0, 0, 1, 3],  # a
            [0, 0, 0, 3],  # b
            [0, 0, 0, 0],  # t
        ]
    cost_matrix = [
            # s a  b  t
            [0, 1, 1, 0],  # s
            [0, 0, 1, 5],  # a
            [0, 0, 0, 1],  # b
            [0, 0, 0, 0],  # t
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
