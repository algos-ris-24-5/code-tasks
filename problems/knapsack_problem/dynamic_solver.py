from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum


class DynamicSolver(KnapsackAbstractSolver):
    def init(self, weights, costs, weight_limit):
        super().init(weights, costs, weight_limit)

    def get_knapsack(self):
        for weight in self.weights:
            if not isinstance(weight, (int, float)):
                raise ValueError(ErrorMessageEnum.FLOAT_WEIGHT)
            if isinstance(weight, float) and not weight.is_integer():
                raise ValueError(ErrorMessageEnum.FLOAT_WEIGHT)

        n = self.item_cnt
        W = self.weight_limit
        weights_int = [int(w) for w in self.weights]
        costs = self.costs

        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            current_weight = weights_int[i - 1]
            current_cost = costs[i - 1]
            for w in range(W + 1):
                if current_weight > w:
                    dp[i][w] = dp[i - 1][w]
                else:
                    dp[i][w] = max(
                        dp[i - 1][w],
                        dp[i - 1][w - current_weight] + current_cost
                    )

        selected_items = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(i - 1)
                w -= weights_int[i - 1]
        selected_items.reverse()

        return KnapsackSolution(dp[n][W], selected_items)

if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = DynamicSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
