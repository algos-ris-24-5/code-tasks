from collections import deque
from math import inf
from network_flow.data_types import NetworkVerticesData
from network_flow.network_validator import NetworkValidator

CAPACITY_MATRIX_NAME = "Таблица пропускных способностей"


class MaxFlowCalculator:
    """Класс для решения задачи поиска максимального потока в сети"""

    def __init__(self, capacity_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        """

        NetworkValidator.validate_matrix(capacity_matrix, CAPACITY_MATRIX_NAME)
        vertices = MaxFlowCalculator.split_vertices_by_types(capacity_matrix)
        NetworkValidator.validate_vertices(vertices, CAPACITY_MATRIX_NAME)

        self._capacity_matrix = capacity_matrix
        self._order = len(capacity_matrix)
        self._source_idx = vertices.sources[0]
        self._sink_idx = vertices.sinks[0]

        self._residual_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if capacity_matrix[row_idx][col_idx]:
                    self._residual_matrix[row_idx][col_idx] = self._capacity_matrix[
                        row_idx
                    ][col_idx]

        self._max_flow = None
        self._flow_matrix = None
        # Процедура _calculate_max_flow должна в ходе выполнения заполнить атрибуты _flow_matrix и _max_flow
        self._calculate_max_flow()

    @property
    def max_flow(self) -> int:
        """Возвращает максимальное значение потока"""
        return self._max_flow

    @property
    def flow_matrix(self) -> tuple[tuple[int]]:
        """Возвращает матрицу локальных потоков"""
        return tuple([tuple(row) for row in self._flow_matrix])

    @staticmethod
    def split_vertices_by_types(matrix) -> NetworkVerticesData:
        """
        Разделяет вершины сети на три категории: источники, стоки и транзитные вершины.

        :param matrix: Квадратная матрица пропускных способностей графа.
        :type matrix: list[list[int]]
        :return: Данные о вершинах сети, содержащие источники, стоки и транзиты.
        :rtype: NetworkVerticesData
        """
        sources = []
        sinks = []
        transits = []

        order = len(matrix)
        for i in range(order):
            is_source = all(matrix[j][i] == 0 for j in range(order))
            is_sink = all(matrix[i][j] == 0 for j in range(order))

            if is_source:
                sources.append(i)
            elif is_sink:
                sinks.append(i)
            else:
                transits.append(i)

        return NetworkVerticesData(sources, sinks, transits)

    def _calculate_max_flow(self) -> None:
        """Вычисляет максимальный поток в сети с использованием алгоритма Форда-Фалкерсона"""
        self._flow_matrix = [[0] * self._order for _ in range(self._order)]
        self._max_flow = 0

        while True:
            augmenting_path = self._find_augmenting_path()
            if not augmenting_path:
                break
            
            self._increase_flow(augmenting_path)

        self._set_flow_matrix_by_residual_matrix()

    def _set_flow_matrix_by_residual_matrix(self):
        """Обновляет матрицу локальных потоков на основе остаточной сети"""
        for i in range(self._order):
            for j in range(self._order):
                if self._capacity_matrix[i][j] > 0:
                    self._flow_matrix[i][j] = (
                        self._capacity_matrix[i][j] - self._residual_matrix[i][j]
                    )

    def _find_augmenting_path(self):
        """Возвращает найденный увеличивающий путь в сети"""
        parent = [-1] * self._order
        queue = deque([self._source_idx])
        parent[self._source_idx] = self._source_idx

        while queue:
            u = queue.popleft()
            if u == self._sink_idx:
                path = []
                curr = self._sink_idx
                while curr != self._source_idx:
                    prev = parent[curr]
                    path.append((prev, curr))
                    curr = prev
                return path[::-1]

            for v in range(self._order):
                if parent[v] == -1 and self._residual_matrix[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        return None

    def _increase_flow(self, augmenting_path):
        """Корректирует остаточную сеть для увеличения потока в сети с использованием
        найденного увеличивающего пути"""
        path_flow = self._residual_matrix[augmenting_path[0][0]][augmenting_path[0][1]]
        for u, v in augmenting_path:
            path_flow = min(path_flow, self._residual_matrix[u][v])

        for u, v in augmenting_path:
            self._residual_matrix[u][v] -= path_flow
            self._residual_matrix[v][u] += path_flow
        
        self._max_flow += path_flow


if __name__ == "__main__":
    vertex_names = ["s", "a", "b", "c", "d", "t"]
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока в сети:")
    max_flow_data = MaxFlowCalculator(capacity_matrix)
    print("Величина максимального потока:", max_flow_data.max_flow)
    print("Матрица локальных потоков")
    for row in max_flow_data.flow_matrix:
        print(row)
