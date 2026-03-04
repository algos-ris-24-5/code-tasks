from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator
from shortest_path.bellman_ford import (
    NegativeLoopBellmanFordError,
    bellman_ford,
    restore_path,
)

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
        super().__init__(capacity_matrix)

        self._cost_matrix = cost_matrix
        self._residual_matrix, self._cost_residual_matrix = self._get_residual_matrices()
        self._minimize_cost()
        self._min_cost = self._get_cost_by_flow()

    @property
    def min_cost(self) -> int:
        """Возвращает минимальную стоимость потока"""
        return self._min_cost

    def _minimize_cost(self) -> None:
        """Осуществляет минимизацию стоимости максимального потока
        посредством поиска и удаления отрицательных циклов в остаточной сети."""
        while True:
            cycle_found = False
            for start in range(self._order):
                negative_loop = self._find_negative_loop(start)
                if negative_loop:
                    self._remove_negative_loop(negative_loop)
                    cycle_found = True
                    break
            if not cycle_found:
                break
        
        self._min_cost = self._get_cost_by_flow()

    def _find_negative_loop(self, start_vertex_idx) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети"""
        n = self._order

        distance = [0] * n
        predecessor = [-1] * n

        active_edges = []
        for i in range(n):
            for j in range(n):
                if self._residual_matrix[i][j] > 0:
                    active_edges.append((i, j, self._cost_residual_matrix[i][j]))

        changed_vertex = -1
        for phase in range(n):
            changed_vertex = -1
            for src, dst, edge_cost in active_edges:
                if distance[src] + edge_cost < distance[dst]:
                    distance[dst] = distance[src] + edge_cost
                    predecessor[dst] = src
                    changed_vertex = dst       
        if changed_vertex == -1:
            return []

        cycle_member = changed_vertex
        for _ in range(n):
            cycle_member = predecessor[cycle_member]

        return self._extract_cycle_path(predecessor, cycle_member)

    def _extract_cycle_path(self, predecessor: list[int], start_node: int) -> list[int]:
        """Извлекает путь цикла из предков"""
        cycle_path = [start_node]
        current = predecessor[start_node]
        
        while current != start_node:
            cycle_path.append(current)
            current = predecessor[current]
        
        cycle_path.append(start_node)

        return list(reversed(cycle_path))

    def _remove_negative_loop(self, loop) -> None:
        """Удаляет цикл отрицательной стоимости из остаточных сетей"""
        if len(loop) < 2:
            return
 
        min_available = inf
        for idx in range(len(loop) - 1):
            from_vert = loop[idx]
            to_vert = loop[idx + 1]
            current_cap = self._residual_matrix[from_vert][to_vert]
            if current_cap > 0:
                min_available = min(min_available, current_cap)
        
        if min_available == inf or min_available <= 0:
            return
        
  
        for idx in range(len(loop) - 1):
            from_vert = loop[idx]
            to_vert = loop[idx + 1]
  
            self._residual_matrix[from_vert][to_vert] -= min_available
            self._residual_matrix[to_vert][from_vert] += min_available

            if self._residual_matrix[to_vert][from_vert] > 0:
                self._cost_residual_matrix[to_vert][from_vert] = -self._cost_residual_matrix[from_vert][to_vert]
            
            if self._residual_matrix[from_vert][to_vert] == 0:
                self._cost_residual_matrix[from_vert][to_vert] = 0

            if self._capacity_matrix[from_vert][to_vert] > 0:
                self._flow_matrix[from_vert][to_vert] -= min_available
            else:
                self._flow_matrix[to_vert][from_vert] += min_available

    def _get_residual_matrices(self):
        """Возвращает остаточные сети на основе матриц потоков и пропускных способностей"""
        size = self._order
        residual = [[0] * size for _ in range(size)]
        cost_residual = [[0] * size for _ in range(size)]
            
        for row in range(size):
            for col in range(size):
                current_flow = self._flow_matrix[row][col]
                remaining = self._capacity_matrix[row][col] - current_flow
                transport_cost = self._cost_matrix[row][col]
                
                if current_flow > 0:
                    residual[row][col] = current_flow
                    cost_residual[row][col] = -transport_cost
                
                if remaining > 0:
                    residual[col][row] = remaining
                    cost_residual[col][row] = transport_cost
        
        return residual, cost_residual

    def _get_cost_by_flow(self) -> int:
        """Возвращает суммарную стоимость транспортировки"""
        total = 0
        for i in range(self._order):
            for j in range(self._order):
                if self._flow_matrix[i][j] > 0:
                    total += self._flow_matrix[i][j] * self._cost_matrix[i][j]
        return total


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