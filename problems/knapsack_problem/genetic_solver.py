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
        self.__population_cnt = int(min(2**self.item_cnt / 2, POPULATION_LIMIT))
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
            solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return solver.get_knapsack()
        
        best_fitness = -1
        best_key = None
        stagnation_counter = 0
        stagnation_limit = max(10, epoch_cnt // 10)
        
        for epoch in range(epoch_cnt):
            # Обновляем фитнес для всех особей
            items_list = []
            for key in list(self.__population.keys()):
                self.__population[key] = self.__get_fit(key)
                items_list.append((key, self.__population[key]))
            
            # Сортируем по фитнесу
            items_list.sort(key=lambda x: x[1], reverse=True)
            
            # Проверяем улучшение
            current_best = items_list[0][1]
            if current_best > best_fitness:
                best_fitness = current_best
                best_key = items_list[0][0]
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            
            # Ранняя остановка, если нет улучшений
            if stagnation_counter >= stagnation_limit:
                break
            
            # Элитизм - сохраняем 10% лучших
            elite_count = max(1, self.__population_cnt // 10)
            new_population = {}
            for i in range(elite_count):
                key, fitness = items_list[i]
                new_population[key] = fitness
            
            # Сильнейшие для скрещивания (50% лучших)
            strongest = [key for key, _ in items_list[:max(2, self.__population_cnt // 2)]]
            
            # Заполняем остальную часть популяции
            attempts = 0
            max_attempts = self.__population_cnt * 5
            
            while len(new_population) < self.__population_cnt and attempts < max_attempts:
                parent1 = rnd.choice(strongest)
                parent2 = rnd.choice(strongest)
                
                child1, child2 = self.__cross_items(parent1, parent2)
                
                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)
                
                if child1 not in new_population:
                    fitness1 = self.__get_fit(child1)
                    if fitness1 > 0:
                        new_population[child1] = fitness1
                
                if len(new_population) < self.__population_cnt and child2 not in new_population:
                    fitness2 = self.__get_fit(child2)
                    if fitness2 > 0:
                        new_population[child2] = fitness2
                
                attempts += 1
            
            # Если не удалось заполнить, добавляем лучших из предыдущей популяции
            if len(new_population) < self.__population_cnt:
                for key, fitness in items_list:
                    if key not in new_population:
                        new_population[key] = fitness
                        if len(new_population) >= self.__population_cnt:
                            break
            
            self.__population = new_population
        
        # Если не нашли лучшего, ищем сейчас
        if best_key is None:
            best_key = max(self.__population.items(), key=lambda x: x[1])[0]
            best_fitness = self.__population[best_key]
        
        best_binary = self.__mask.format(best_key)
        best_items = [i for i, bit in enumerate(best_binary) if bit == '1']
        
        return KnapsackSolution(cost=best_fitness, items=best_items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population = {}
        attempts = 0
        max_attempts = population_cnt * 5
        
        while len(population) < population_cnt and attempts < max_attempts:
            item = 0
            # С вероятностью 30% включаем каждый предмет
            for i in range(self.item_cnt):
                if rnd.random() < 0.3:
                    item |= (1 << i)
            
            fitness = self.__get_fit(item)
            if fitness > 0 and item not in population:
                population[item] = fitness
            attempts += 1
        
        if len(population) == 0:
            population[0] = self.__get_fit(0)
        
        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Равномерное скрещивание."""
        child1 = 0
        child2 = 0
        
        for i in range(self.item_cnt):
            if rnd.random() < 0.5:
                if ancestor1 & (1 << i):
                    child1 |= (1 << i)
                if ancestor2 & (1 << i):
                    child2 |= (1 << i)
            else:
                if ancestor2 & (1 << i):
                    child1 |= (1 << i)
                if ancestor1 & (1 << i):
                    child2 |= (1 << i)
        
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        """Мутация особи с вероятностью 5%."""
        mutation_rate = 0.05
        for i in range(self.item_cnt):
            if rnd.random() < mutation_rate:
                item_set ^= (1 << i)
        return item_set

    def __get_fit(self, item: int) -> int:
        """Вычисляет значение фитнес-функции для особи."""
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