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
        if self.order == 1:
            return TspSolution(0, [0])
        
        cities = list(range(1, self.order))
        
        if not cities:
            return TspSolution(None, [])
        
        permutations = generate_permutations(cities)
        
        min_distance = None
        best_path = []
        
        for perm in permutations:
            path = [0] + list(perm) + [0]
            
            valid_path = True
            for i in range(1, len(path)):
                if self._dist_matrix[path[i-1]][path[i]] is None:
                    valid_path = False
                    break
            
            if valid_path:
                distance = self.get_distance(self._dist_matrix, path)
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    best_path = path
        
        if min_distance is None:
            return TspSolution(None, [])
        
        return TspSolution(min_distance, best_path)


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

