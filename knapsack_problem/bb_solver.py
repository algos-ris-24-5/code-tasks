import heapq
from collections import namedtuple

from knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

KnapsackItem = namedtuple("KnapsackItem", ["weight", "cost", "price", "source_idx"])
BranchNode = namedtuple("BranchNode", ["level", "taken", "bound"])


class BranchAndBoundSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием метода ветвей и границ."""
        items = [
            KnapsackItem(weight, cost, cost / weight, idx)
            for idx, (weight, cost) in enumerate(zip(self.weights, self.costs))
        ]
        items.sort(key=lambda x: x.price, reverse=True)

        return self._solve(items)

    def _solve(self, items: list) -> KnapsackSolution:
        """Реализует поиск оптимального решения методом ветвей и границ."""
        max_cost = 0
        best_items = []
        queue = []
        
        initial_taken = (0, 0, [])
        initial_bound = self._get_bound(0, initial_taken, items)
        
        root = BranchNode(0, initial_taken, initial_bound)
        heapq.heappush(queue, (-root.bound, root))

        while queue:
            neg_bound, node = heapq.heappop(queue)
            
            if -neg_bound <= max_cost or node.level == len(items):
                continue

            item = items[node.level]
            current_weight, current_cost, current_indices = node.taken

            if current_weight + item.weight <= self.weight_limit:
                take_weight = current_weight + item.weight
                take_cost = current_cost + item.cost
                take_indices = current_indices + [item.source_idx]
                
                if take_cost > max_cost:
                    max_cost = take_cost
                    best_items = take_indices

                take_taken = (take_weight, take_cost, take_indices)
                take_bound = self._get_bound(node.level + 1, take_taken, items)
                if take_bound > max_cost:
                    take_node = BranchNode(node.level + 1, take_taken, take_bound)
                    heapq.heappush(queue, (-take_bound, take_node))

            dont_taken = (current_weight, current_cost, current_indices)
            dont_bound = self._get_bound(node.level + 1, dont_taken, items)
            if dont_bound > max_cost:
                dont_node = BranchNode(node.level + 1, dont_taken, dont_bound)
                heapq.heappush(queue, (-dont_bound, dont_node))

        return KnapsackSolution(max_cost, best_items)

    def _get_bound(self, level, taken, items):
        """Вычисляет верхнюю границу для текущей ветви (верхнюю оценку стоимости)."""
        current_weight, current_cost = taken[0], taken[1]
        bound = float(current_cost)
        total_weight = current_weight
        n = len(items)

        for i in range(level, n):
            if total_weight + items[i].weight <= self.weight_limit:
                total_weight += items[i].weight
                bound += items[i].cost
            else:
                bound += (self.weight_limit - total_weight) * items[i].price
                break

        return bound


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BranchAndBoundSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )