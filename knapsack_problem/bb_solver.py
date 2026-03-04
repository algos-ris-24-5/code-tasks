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

        self.n = len(items)
        self.items = items
        self.best_cost = 0
        self.best_selection = []

        self._search(0, 0, 0, [])

        return KnapsackSolution(
            cost=self.best_cost,
            items=sorted(self.best_selection)
        )

    def _search(self, level: int, curr_weight: int, curr_cost: int, selection: list):
        if level == self.n:
            if curr_cost > self.best_cost:
                self.best_cost = curr_cost
                self.best_selection = selection[:]
            return

        bound_no = self._get_bound(level, curr_weight, curr_cost)
        if bound_no > self.best_cost:
            self._search(level + 1, curr_weight, curr_cost, selection)

        item = self.items[level]
        if curr_weight + item.weight <= self.weight_limit:
            bound_yes = self._get_bound(level + 1, curr_weight + item.weight, curr_cost + item.cost)
            if bound_yes > self.best_cost:
                new_selection = selection + [item.source_idx]
                self._search(level + 1, curr_weight + item.weight, curr_cost + item.cost, new_selection)

    def _get_bound(self, level: int, curr_weight: int, curr_cost: int) -> float:
        if level == self.n:
            return curr_cost

        bound = curr_cost
        remain_capacity = self.weight_limit - curr_weight

        if remain_capacity <= 0:
            return bound

        for i in range(level, self.n):
            item = self.items[i]

            if item.weight == 0:
                bound += item.cost
                continue

            if remain_capacity >= item.weight:
                bound += item.cost
                remain_capacity -= item.weight
            else:
                bound += item.price * remain_capacity
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