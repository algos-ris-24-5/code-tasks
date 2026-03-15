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
            solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return solver.get_knapsack()

        pop_cnt = int(self.__population_cnt)

        for _ in range(epoch_cnt):
            new_population = {}
            
            pop_items = list(self.__population.keys())
            pop_fits = list(self.__population.values())
            
            # Элитизм: берем самых сильных особей в новое поколение (10% лучших)
            # Это гарантирует, что лучший результат не будет утерян
            sorted_items = sorted(pop_items, key=lambda k: self.__population[k], reverse=True)
            elite_cnt = max(1, pop_cnt // 10)
            for i in range(min(elite_cnt, len(sorted_items))):
                item = sorted_items[i]
                new_population[item] = self.__population[item]
                
            total_fit = sum(pop_fits)
            
            if total_fit == 0:
                probs = [1.0 / len(pop_fits)] * len(pop_fits)
            else:
                probs = [fit / total_fit for fit in pop_fits]
                
            attempts = 0
            max_attempts = pop_cnt * 2  # Снизили лимит для предотвращения долгих зависаний
            
            # ВАЖНО: rnd.choices каждый раз вычисляет кумулятивную сумму весов (O(N)).
            # Если вызывать его внутри while, это дает миллиарды лишних операций!
            # Генерируем всех родителей сразу:
            pool_size = max_attempts * 2 + pop_cnt * 2
            parents_pool = rnd.choices(pop_items, weights=probs, k=pool_size)
            p_idx = 0
            
            while len(new_population) < pop_cnt and attempts < max_attempts:
                if p_idx + 1 >= len(parents_pool):
                    parents_pool.extend(rnd.choices(pop_items, weights=probs, k=pool_size))
                    
                parent1 = parents_pool[p_idx]
                parent2 = parents_pool[p_idx + 1]
                p_idx += 2
                
                child1, child2 = self.__cross_items(parent1, parent2)
                
                if rnd.random() < 0.1:
                    child1 = self.__mutation(child1)
                if rnd.random() < 0.1:
                    child2 = self.__mutation(child2)
                    
                added_new = False
                if child1 not in new_population:
                    new_population[child1] = self.__get_fit(child1)
                    added_new = True
                if len(new_population) < pop_cnt and child2 not in new_population:
                    new_population[child2] = self.__get_fit(child2)
                    added_new = True
                    
                if added_new:
                    attempts = 0
                else:
                    attempts += 1
                    
            if len(new_population) < pop_cnt:
                max_val = (1 << self.item_cnt) - 1
                gen_attempts = 0
                while len(new_population) < pop_cnt and gen_attempts < pop_cnt * 5:
                    item = rnd.randint(0, max_val)
                    if item not in new_population:
                        new_population[item] = self.__get_fit(item)
                    gen_attempts += 1
                    
            self.__population = new_population

        best_item_key = max(self.__population.keys(), key=lambda k: self.__population[k])
        best_cost = self.__population[best_item_key]
        bin_str = self.__mask.format(best_item_key)
        best_items = [i for i, bit in enumerate(bin_str) if bit == '1']
        
        return KnapsackSolution(cost=best_cost, items=best_items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population = {}
        max_val = (1 << self.item_cnt) - 1
        attempts = 0
        while len(population) < population_cnt and attempts < population_cnt * 10:
            item = rnd.randint(0, max_val)
            if item not in population:
                population[item] = self.__get_fit(item)
            attempts += 1
        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        if self.item_cnt <= 1:
            return ancestor1, ancestor2
        point = rnd.randint(1, self.item_cnt - 1)
        mask1 = (1 << point) - 1
        mask2 = ((1 << self.item_cnt) - 1) ^ mask1
        
        child1 = (ancestor1 & mask2) | (ancestor2 & mask1)
        child2 = (ancestor2 & mask2) | (ancestor1 & mask1)
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        bit = rnd.randint(0, self.item_cnt - 1)
        return item_set ^ (1 << bit)

    def __get_fit(self, item: int) -> int:
        bin_str = self.__mask.format(item)
        selected = [bit == '1' for bit in bin_str]
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
