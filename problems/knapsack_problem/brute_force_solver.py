from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)


class BruteForceSolver(KnapsackAbstractSolver):
    def get_knapsack(self) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием полного перебора."""
        max_cost = 0
        best_items = []
        for combination in range(1, 2**self.item_cnt):
            binary_str = bin(combination)[2:].zfill(self.item_cnt)
            selected_items = [bit == '1' for bit in binary_str]
            current_cost = self.get_cost(selected_items)
            if current_cost > max_cost:
                max_cost = current_cost
                best_items = [item_index for item_index in range(self.item_cnt) if selected_items[item_index]]
        return KnapsackSolution(cost=max_cost, items=best_items)


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = BruteForceSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
