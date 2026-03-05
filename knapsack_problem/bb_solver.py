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
        if self.item_cnt == 0:
            return KnapsackSolution(0, [])
        
        max_profit = 0
        best_items = []
        items = [
            KnapsackItem(weight, cost, cost / weight, idx)
            for idx, (weight, cost) in enumerate(zip(self.weights, self.costs))
        ]
        items.sort(key=lambda x: x.price, reverse=True)
        queue = []

        largest_bound = self._get_bound(-1, [False]*self.item_cnt, items)
        heapq.heappush(queue, ((-1)*largest_bound, 1, BranchNode(-1, [False]*self.item_cnt, largest_bound)))
        while (len(queue) > 0):
            cur_node = heapq.heappop(queue)[2]

            if cur_node.bound <= max_profit: break
            if cur_node.level == (self.item_cnt - 1): continue

            new_taken = cur_node.taken[:]
            new_taken[cur_node.level + 1] = True
            weights = sum([items[i].weight for i in range(cur_node.level+2) if new_taken[i]])
            if weights <= self._weight_limit:
                take_node = BranchNode(cur_node.level + 1, new_taken, self._get_bound(cur_node.level + 1, new_taken, items))

                if take_node.bound > max_profit:
                    heapq.heappush(queue, ((-1)*take_node.bound, (-1)*(cur_node.level + 1), take_node))

                profit = sum([items[i].cost for i in range(cur_node.level+2) if new_taken[i]])
                if profit > max_profit:
                    max_profit = profit
                    best_items = new_taken
            
            not_take_node = BranchNode(cur_node.level + 1, cur_node.taken, self._get_bound(cur_node.level + 1, cur_node.taken, items))
            if not_take_node.bound > max_profit:
                heapq.heappush(queue, ((-1)*not_take_node.bound, (-1)*(cur_node.level + 1), not_take_node))

        return KnapsackSolution(max_profit, [items[idx].source_idx for idx, item in enumerate(best_items) if item])

    def _get_bound(self, level, taken, items):
        cur_weight = 0
        worth = 0
        if level == -1:
            return items[0].price*self._weight_limit

        for i in range(level + 1):
            if (taken[i]):
                cur_weight += items[i].weight
                worth += items[i].cost

        if cur_weight > self._weight_limit:
            return -1

        if level + 1 < self.item_cnt:
            worth += (self._weight_limit - cur_weight) * items[(level + 1)].price

        return worth


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