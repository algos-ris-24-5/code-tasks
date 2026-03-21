import random as rnd

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 1000
"""Предельный размер популяции."""

EPOCH_CNT = 100
"""Количество поколений по умолчанию."""

BRUTE_FORCE_BOUND = 5
"""Размер входных данных задачи, до которого используется полный перебор."""


class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный
    перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.

    """

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создает объект класса для решения задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = min(2**self.item_cnt / 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            brute_solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return brute_solver.get_knapsack()

        for _ in range(epoch_cnt):
            new_population = {}

            elite_cnt = max(1, int(self.__population_cnt * 0.1))
            sorted_items = sorted(self.__population.items(), key=lambda x: x[1], reverse=True)

            for i in range(elite_cnt):
                individual = sorted_items[i][0]
                fit = self.__get_fit(individual)
                if fit > 0:
                    new_population[individual] = fit

            keys = list(self.__population.keys())

            while len(new_population) < self.__population_cnt:
                parent1 = self.__tournament_selection(keys)
                parent2 = self.__tournament_selection(keys)

                child1, child2 = self.__cross_items(parent1, parent2)

                fit1 = self.__get_fit(child1)
                if child1 in new_population or fit1 == 0:
                    child1 = self.__mutation(child1)
                    fit1 = self.__get_fit(child1)

                fit2 = self.__get_fit(child2)
                if child2 in new_population or fit2 == 0:
                    child2 = self.__mutation(child2)
                    fit2 = self.__get_fit(child2)

                new_population[child1] = fit1
                if len(new_population) < self.__population_cnt:
                    new_population[child2] = fit2

            self.__population = new_population

        best_individual = None
        best_fit = -1
        for individual, fit in self.__population.items():
            if fit > best_fit:
                best_fit = fit
                best_individual = individual

        if best_individual is None:
            return KnapsackSolution(cost=0, items=[])

        best_mask = best_individual
        items_indices = [i for i in range(self.item_cnt) if (best_mask >> i) & 1]

        return KnapsackSolution(cost=best_fit, items=items_indices)

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        population = {}
        max_value = (1 << self.item_cnt) - 1

        while len(population) < population_cnt:
            individual = rnd.randint(0, max_value)
            if individual not in population:
                population[individual] = self.__get_fit(individual)

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        point1 = rnd.randint(1, self.item_cnt - 1)
        point2 = rnd.randint(point1, self.item_cnt - 1)

        mask_left = (1 << point1) - 1
        mask_middle = ((1 << (point2 - point1)) - 1) << point1
        mask_right = ((1 << (self.item_cnt - point2)) - 1) << point2

        child1 = (ancestor1 & mask_left) | (ancestor2 & mask_middle) | (ancestor1 & mask_right)
        child2 = (ancestor2 & mask_left) | (ancestor1 & mask_middle) | (ancestor2 & mask_right)

        return child1, child2

    def __mutation(self, item_set: int) -> int:
        mutation_rate = 1.0 / self.item_cnt
        max_attempts = 10

        for _ in range(max_attempts):
            mask = 0
            for i in range(self.item_cnt):
                if rnd.random() < mutation_rate:
                    mask |= (1 << i)

            mutated = item_set ^ mask

            if self.__get_fit(mutated) > 0:
                return mutated

        for i in range(self.item_cnt):
            mutated = item_set ^ (1 << i)
            if self.__get_fit(mutated) > 0:
                return mutated

        return item_set

    def __get_fit(self, item_set: int) -> int:
        total_weight = 0
        total_cost = 0
        for i in range(self.item_cnt):
            if (item_set >> i) & 1:
                total_weight += self.weights[i]
                if total_weight > self.weight_limit:
                    return 0
                total_cost += self.costs[i]
        return total_cost

    def __tournament_selection(self, keys) -> int:
        candidate1, candidate2 = rnd.sample(keys, 2)
        return candidate1 if self.__population[candidate1] > self.__population[candidate2] else candidate2


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")
    solver = GeneticSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
