from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum
from problems.knapsack_problem.errors.error_message_template import ErrorMessageTemplateEnum
from problems.knapsack_problem.errors.constants import WEIGHTS, COSTS


class DynamicSolver(KnapsackAbstractSolver):
    def __init__(self, weights, costs, weight_limit):
        if not isinstance(weights, list):
            raise TypeError(ErrorMessageTemplateEnum.NOT_LIST.format(WEIGHTS))
        if not weights:
            raise ValueError(ErrorMessageTemplateEnum.EMPTY_LIST.format(WEIGHTS))

        validated_weights = []
        for w in weights:
            if isinstance(w, bool): 
                raise TypeError(ErrorMessageTemplateEnum.NOT_INT.format(WEIGHTS))
            if not isinstance(w, (int, float)):
                raise TypeError(ErrorMessageTemplateEnum.NOT_INT.format(WEIGHTS))
            if isinstance(w, float):
                if not w.is_integer():
                    raise ValueError("Вес предмета не является целым числом")
                w = int(w)
            if w <= 0:
                raise ValueError(ErrorMessageTemplateEnum.NOT_POS.format(WEIGHTS))
            validated_weights.append(w)

        if not isinstance(costs, list):
            raise TypeError(ErrorMessageTemplateEnum.NOT_LIST.format(COSTS))
        if not costs:
            raise ValueError(ErrorMessageTemplateEnum.EMPTY_LIST.format(COSTS))
        validated_costs = []
        for c in costs:
            if isinstance(c, bool):
                raise TypeError(ErrorMessageTemplateEnum.NOT_INT.format(COSTS))
            if not isinstance(c, int):
                raise TypeError(ErrorMessageTemplateEnum.NOT_INT.format(COSTS))
            if c <= 0:
                raise ValueError(ErrorMessageTemplateEnum.NOT_POS.format(COSTS))
            validated_costs.append(c)

        if len(validated_weights) != len(validated_costs):
            raise ValueError(ErrorMessageEnum.LENGTHS_NOT_EQUAL)

        if not isinstance(weight_limit, int) or isinstance(weight_limit, bool):
            raise TypeError(ErrorMessageEnum.NOT_INT_WEIGHT_LIMIT)
        if weight_limit <= 0:
            raise ValueError(ErrorMessageEnum.NOT_POS_WEIGHT_LIMIT)
        if weight_limit < min(validated_weights):
            raise ValueError(ErrorMessageEnum.LESS_WEIGHT_LIMIT)

        super().__init__(validated_weights, validated_costs, weight_limit)

    def get_knapsack(self):
        n = self.item_cnt
        W = self.weight_limit
        weights_int = self.weights
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
