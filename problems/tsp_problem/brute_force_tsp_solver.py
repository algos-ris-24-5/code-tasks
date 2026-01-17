from math import inf
from problems.tsp_problem.tsp_abs_solver import (
    AbstractTspSolver,
    TspSolution,
)
from generators.permutation_generator import generate_permutations


class BruteForceTspSolver(AbstractTspSolver):
    def get_tsp_solution(self) -> TspSolution:
        """Возвращает решение задачи коммивояжера в виде именованного кортежа с полями:
        - distance - кратчайшее расстояние,
        - path - список с индексами вершин на кратчайшем маршруте.
        """
        n = len(self._dist_matrix)
        
        if n == 1:
            return TspSolution(0, [0])
        
        cities = list(range(1, n))
        
        if not cities:
            return TspSolution(None, [])
        
        permutations = generate_permutations(cities)
        
        min_distance = None
        best_path = []
        
        for perm in permutations:
            path = [0] + list(perm) + [0]
            distance = self._calculate_path_distance(path)
            
            if distance is not None:
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    best_path = path
        
        if min_distance is None:
            return TspSolution(None, [])
        
        return TspSolution(min_distance, best_path)
    
    def _calculate_path_distance(self, path: list[int]) -> float:
        distance = 0.0
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            weight = self._dist_matrix[src][trg]
            
            if weight is None:
                return None
            
            distance += weight
        
        return distance


if __name__ == "__main__":
    print("Пример решения задачи коммивояжёра\n\nМатрица расстояний:")
    matrix = [
        [None, 12.0, 9.0, 9.0, 12.0],
        [9.0, None, 8.0, 19.0, 15.0],
        [7.0, 1.0, None, 17.0, 11.0],
        [5.0, 9.0, 12.0, None, 16.0],
        [14.0, 6.0, 12.0, 22.0, None],
    ]
    for row in matrix:
        print(row)

    solver = BruteForceTspSolver(matrix)
    result = solver.get_tsp_solution()
    print(f"Минимальное расстояние: {result.distance}, " f"Маршрут: {result.path}")