from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum

class DynamicSolver(KnapsackAbstractSolver):
    def get_knapsack(self):
        """
        Решает задачу о рюкзаке с использованием метода динамического программирования.

        :return: максимально возможная общая стоимость и список индексов выбранных предметов
        :rtype: KnapsackSolution
        """
        for weight in self.weights:
            if not float(weight).is_integer():
                raise ValueError(ErrorMessageEnum.FLOAT_WEIGHT)
        
        n = self.item_cnt
        W = self.weight_limit
        
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            current_weight = self.weights[i-1]
            current_cost = self.costs[i-1]
            
            for w in range(W + 1):
                if current_weight > w:
                    dp[i][w] = dp[i-1][w]
                else:
                    dp[i][w] = max(
                        dp[i-1][w],  # не берем предмет
                        dp[i-1][w - current_weight] + current_cost  # берем предмет
                    )
        selected_items = []
        current_weight = W
        for i in range(n, 0, -1):
            if dp[i][current_weight] != dp[i-1][current_weight]:
                selected_items.append(i-1)
                current_weight -= self.weights[i-1]
        selected_items.reverse()
        return self.KnapsackSolution(dp[n][W], selected_items)

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
