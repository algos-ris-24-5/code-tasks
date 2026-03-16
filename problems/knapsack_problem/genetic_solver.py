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
        self.__best_specimen: int = self.__find_best_individual()
        self.__best_fitness: int = self.__get_fit(self.__best_specimen)

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
        """
        Решает задачу о рюкзаке с использованием генетического алгоритма
        
        :param epoch_cnt: Количество популяций для генетического алгоритма
        :return: Решение задачи о рюкзаке
        """
        
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            brute_solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return brute_solver.get_knapsack()
        
        for generation in range(epoch_cnt):
            selected = self.__selection()
            offspring = self.__crossover(selected)
            mutated_offspring = self.__mutation(offspring)
            self.__population = self.__generate_new_population(selected, mutated_offspring)

            current_best = self.__find_best_individual()
            current_fitness = self.__get_fit(current_best)

            if current_fitness > self.__best_fitness:
                self.__best_fitness = current_fitness
                self.__best_specimen = current_best

            if generation >= epoch_cnt - 1:
                break

        selected_items = []
        for i in range(self.item_cnt):
            if (self.__best_specimen >> i) & 1:
                selected_items.append(i)

        return KnapsackSolution(cost=self.__best_fitness, items=selected_items)

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """
        Инициализация начальной популяции случайными особями
        Создает популяцию заданного размера со случайными комбинациями предметов

        :return: Словарь особей с их значениями фитнес-функции
        """
        population = {}
        max_items = 2**self.item_cnt
        max_iterations = 500

        current_iteration = 0
        if max_items > POPULATION_LIMIT:
            while len(population) < population_cnt:
                current_iteration += 1
                if max_iterations < current_iteration: break

                individual = rnd.randint(0, max_items - 1)
                if individual not in population:
                    fitness = self.__get_fit(individual)
                    if fitness > 0:
                        population[individual] = fitness
                        current_iteration = 0
        else:
            for i in range(max_items):
                fitness = self.__get_fit(i)
                if fitness > 0:
                    population[i] = fitness

        return population

    def __generate_new_population(
        self, selected: list[int], offspring: list[int]
    ) -> dict[int, int]:
        """
        Создание новой популяции
        Сохраняет лучших из предков и добавляет потомков

        :param selected: Отобранные особи
        :param offspring: Потомки после мутации
        :return: Новая популяция
        """
        new_population = {}
        max_iterations = 500

        for individual in selected:
            fitness = self.__get_fit(individual)
            if fitness > 0:
                new_population[individual] = fitness

        for individual in offspring:
            if individual not in new_population and len(new_population) < self.__population_cnt:
                fitness = self.__get_fit(individual)
                if fitness > 0:
                    new_population[individual] = fitness

        current_iteration = 0
        while len(new_population) < self.__population_cnt:
            current_iteration += 1
            if max_iterations < current_iteration: break

            individual = rnd.randint(0, 2**self.item_cnt - 1)
            if individual not in new_population:
                fitness = self.__get_fit(individual)
                if fitness > 0:
                    new_population[individual] = fitness
                    current_iteration = 0

        return new_population
    
    def __find_best_individual(self) -> int:
        """
        Поиск лучшей особи в текущей популяции

        :return: Лучшая особь
        """
        return max(self.__population.keys(), key=lambda x: self.__population[x])
    
    def __selection(self) -> list[int]:
        """
        Отбор сильнейших особей для скрещивания
        Сортирует популяцию по фитнес-функции и выбирает половину лучших

        :return: Список отобранных особей
        """
        sorted_population = sorted(
            self.__population.keys(),
            key=lambda x: self.__population[x],
            reverse=True
        )

        best_count = max(2, len(sorted_population) // 2)
        return sorted_population[:best_count]

    def __crossover(self, selected: list[int]) -> list[int]:
        """
        Равномерное скрещивание отобранных особей
        При равномерном скрещивании каждый бит потомка выбирается
        случайно от одного из родителей с одинаковой вероятностью

        :param selected: Список отобранных для скрещивания особей
        :return: Список потомков
        """
        offspring = []

        for i in range(len(selected)):
            for j in range(i + 1, len(selected)):
                if len(offspring) + len(selected) >= self.__population_cnt:
                    return offspring

                ancestor1 = selected[i]
                ancestor2 = selected[j]

                child1, child2 = self.__cross_items(ancestor1, ancestor2)
                offspring.append(child1)
                offspring.append(child2)

        return offspring

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """
        Равномерное скрещивание двух родителей
        Каждый бит потомка выбирается случайно от одного из родителей

        :param ancestor1: Первый предок
        :param ancestor2: Второй предок
        :return: Кортеж из двух потомков
        """
        child1 = 0
        child2 = 0

        for i in range(self.item_cnt):
            bit1 = (ancestor1 >> i) & 1
            bit2 = (ancestor2 >> i) & 1

            if rnd.random() < 0.5:
                child1 |= (bit1 << i)
                child2 |= (bit2 << i)
            else:
                child1 |= (bit2 << i)
                child2 |= (bit1 << i)

        return child1, child2

    def __mutation(self, offspring: list[int]) -> list[int]:
        """
        Мутация потомков
        С заданной вероятностью инвертирует случайный бит особи. Выполняется для всех особей в потомстве

        :param offspring: Список потомков
        :return: Список мутировавших потомков
        """
        mutation_rate = 0.1
        mutated = []

        for individual in offspring:
            if rnd.random() < mutation_rate:
                bit_position = rnd.randint(0, self.item_cnt - 1)
                individual ^= (1 << bit_position)
            mutated.append(individual)

        return mutated

    def __get_fit(self, item: int) -> int:
        """
        Фитнес-функция
        Вычисляет суммарную стоимость предметов в рюкзаке
        Если вес превышает лимит, возвращает 0

        :param item: Особь в виде маски
        :return: Значение фитнес-функции
        """
        total_weight = 0
        total_cost = 0

        for i in range(self.item_cnt):
            if (item >> i) & 1:
                total_weight += self.weights[i]
                total_cost += self.costs[i]

        if total_weight > self.weight_limit:
            return 0

        return total_cost


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
