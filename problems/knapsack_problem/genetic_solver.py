import random as rnd

from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 500
"""Предельный размер популяции."""

EPOCH_CNT = 50
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
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            self.__population_cnt = 0
            self.__population = {}
        else:
            self.__population_cnt = int(min(2**self.item_cnt / 2, POPULATION_LIMIT))
            self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return []
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return solver.get_knapsack()

        best_key = None
        best_fitness = -1

        for _ in range(epoch_cnt):
            items_list = []
            for key in list(self.__population.keys()):
                self.__population[key] = self.__get_fit(key)
                items_list.append((key, self.__population[key]))

            items_list.sort(key=lambda x: x[1], reverse=True)

            if not items_list:
                continue

            current_best_key, current_best_fitness = items_list[0]
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_key = current_best_key

            elite_count = max(1, min(self.__population_cnt // 10, len(items_list)))
            new_population = {}
            for i in range(elite_count):
                key, fitness = items_list[i]
                new_population[key] = fitness

            strongest_count = max(2, min(self.__population_cnt // 2, len(items_list)))
            strongest = [key for key, _ in items_list[:strongest_count]]

            attempts = 0
            max_attempts = self.__population_cnt * 3

            while len(new_population) < self.__population_cnt and attempts < max_attempts:
                if len(strongest) < 2:
                    break

                parent1 = rnd.choice(strongest)
                parent2 = rnd.choice(strongest)

                mask = rnd.getrandbits(self.item_cnt)
                child1 = (parent1 & mask) | (parent2 & ~mask)
                child2 = (parent2 & mask) | (parent1 & ~mask)

                mutation_mask1 = 0
                mutation_mask2 = 0
                for i in range(self.item_cnt):
                    if rnd.random() < 0.05:
                        mutation_mask1 |= (1 << i)
                    if rnd.random() < 0.05:
                        mutation_mask2 |= (1 << i)
                child1 ^= mutation_mask1
                child2 ^= mutation_mask2

                for child in (child1, child2):
                    if len(new_population) < self.__population_cnt and child not in new_population:
                        binary = self.__mask.format(child)
                        selected = [c == '1' for c in binary]
                        fitness = self.get_cost(selected)
                        if fitness > 0:
                            new_population[child] = fitness
                attempts += 1

            if len(new_population) < self.__population_cnt:
                for key, fitness in items_list:
                    if key not in new_population:
                        new_population[key] = fitness
                        if len(new_population) >= self.__population_cnt:
                            break

            self.__population = new_population

        if best_key is None:
            items_list = list(self.__population.items())
            if items_list:
                items_list.sort(key=lambda x: x[1], reverse=True)
                best_key, best_fitness = items_list[0]
            else:
                best_key = 0
                best_fitness = 0

        best_binary = self.__mask.format(best_key)
        best_items = [i for i, bit in enumerate(best_binary) if bit == '1']
        return KnapsackSolution(cost=best_fitness, items=best_items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population = {}
        attempts = 0
        max_attempts = population_cnt * 3

        while len(population) < population_cnt and attempts < max_attempts:
            item = 0
            for i in range(self.item_cnt):
                if rnd.random() < 0.3:
                    item |= (1 << i)

            if item not in population:
                binary = self.__mask.format(item)
                selected = [c == '1' for c in binary]
                fitness = self.get_cost(selected)
                if fitness > 0:
                    population[item] = fitness
            attempts += 1

        if len(population) == 0:
            population[0] = self.get_cost([False] * self.item_cnt)

        return population

    def __get_fit(self, item: int) -> int:
        binary = self.__mask.format(item)
        selected = [c == '1' for c in binary]
        return self.get_cost(selected)


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