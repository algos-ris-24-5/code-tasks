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
        self.__population_cnt = min(2**self.item_cnt // 2, POPULATION_LIMIT)
        self.__population_cnt = max(self.__population_cnt, 10) 
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

    def get_knapsack(self, epoch_cnt=EPOCH_CNT, stagnation_limit=20) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            brute_solver = BruteForceSolver(self._weights, self._costs, self._weight_limit)
            return brute_solver.get_knapsack()

        best_solution = None
        best_cost = -1
        stagnation_counter = 0
        for epoch in range(epoch_cnt):
            for item_set in list(self.__population.keys()):
                self.__population[item_set] = self.__get_fit(item_set)
            if self.__population:
                current_leader = max(self.__population, key=self.__population.get)
                current_fitness = self.__population[current_leader]
                if current_fitness > best_cost:
                    best_cost = current_fitness
                    best_solution = current_leader
                    stagnation_counter = 0
                else:
                    stagnation_counter += 1
                if stagnation_counter >= stagnation_limit:
                    break
            new_population = {}
            sorted_pop = sorted(self.__population.items(), key=lambda x: x[1], reverse=True)
            elite_count = max(1, len(sorted_pop) // 10)
            for i in range(min(elite_count, len(sorted_pop))):
                new_population[sorted_pop[i][0]] = sorted_pop[i][1]
            while len(new_population) < self.__population_cnt:
                ancestor1 = self.__select_parent()
                ancestor2 = self.__select_parent()
                child1, child2 = self.__cross_items(ancestor1, ancestor2)
                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)
                if len(new_population) < self.__population_cnt:
                    new_population[child1] = self.__get_fit(child1)
                if len(new_population) < self.__population_cnt:
                    new_population[child2] = self.__get_fit(child2)
            self.__population = new_population
        if best_solution is not None:
            mask_str = self.__mask.format(best_solution)
            items = [idx for idx, bit in enumerate(mask_str) if bit == '1']
            final_cost = self.get_cost([bit == '1' for bit in mask_str])
            return KnapsackSolution(cost=final_cost, items=items)
        return KnapsackSolution(cost=0, items=[])

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population = {}
        max_val = 2**self.item_cnt
        for _ in range(population_cnt):
            item_set = rnd.randint(0, max_val - 1)
            population[item_set] = self.__get_fit(item_set)
        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        s1 = self.__mask.format(ancestor1)
        s2 = self.__mask.format(ancestor2)
        point = rnd.randint(1, len(s1) - 1)
        res1 = int(s1[:point] + s2[point:], 2)
        res2 = int(s2[:point] + s1[point:], 2)
        return res1, res2

    def __mutation(self, item_set: int) -> int: 
        mutation_rate = 0.1
        for i in range(self.item_cnt):
            if rnd.random() < mutation_rate:
                item_set ^= (1 << i)
        return item_set

    def __get_fit(self, item):
        mask_str = self.__mask.format(item)
        selected = [bit == '1' for bit in mask_str]
        return self.get_cost(selected)

    def __select_parent(self) -> int:
        tournament_size = 3
        candidates = rnd.sample(
            list(self.__population.keys()),
            min(tournament_size, len(self.__population))
        )
        return max(candidates, key=lambda x: self.__population[x])

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