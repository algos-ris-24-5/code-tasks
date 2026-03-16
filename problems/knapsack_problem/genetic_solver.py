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

        total_combinations = 2**self.item_cnt
        if self.item_cnt <= 4:
            self.__population_cnt = total_combinations
        else:
            self.__population_cnt = min(total_combinations // 2, POPULATION_LIMIT)
        
        if self.__population_cnt < 2 and total_combinations >= 2:
            self.__population_cnt = 2
            
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

        try:
            if self.item_cnt <= BRUTE_FORCE_BOUND:
                brute_solver = BruteForceSolver(self._weights, self._costs, self._weight_limit)
                return brute_solver.get_knapsack()

            best_solution = None
            best_cost = 0
            stagnation_counter = 0

            for epoch in range(epoch_cnt):
                self.__population = {k: v for k, v in self.__population.items() if v > 0}

                if not self.__population:
                    self.__population = self.__generate_population(self.__population_cnt)
                    if not self.__population:
                        break
                
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
                
                valid_elites = []
                for item_key, item_fit in sorted_pop:
                    if item_fit > 0:
                        valid_elites.append((item_key, item_fit))
                    else:
                        break
                
                elite_count = max(1, len(sorted_pop) // 10)
                count_to_copy = min(elite_count, len(valid_elites))
                
                for i in range(count_to_copy):
                    new_population[valid_elites[i][0]] = valid_elites[i][1]

                attempts = 0
                max_attempts = self.__population_cnt * 100 


                while len(new_population) < self.__population_cnt and attempts < max_attempts:
                    attempts += 1

                    if len(self.__population) < 2:
                        break 

                    ancestor1 = self.__select_parent()
                    ancestor2 = self.__select_parent()

                    child1, child2 = self.__cross_items(ancestor1, ancestor2)

                    child1 = self.__mutation(child1)
                    child2 = self.__mutation(child2)

                    fit1 = self.__get_fit(child1)
                    if fit1 > 0 and len(new_population) < self.__population_cnt and child1 not in new_population:
                        new_population[child1] = fit1

                    if len(new_population) < self.__population_cnt:
                        fit2 = self.__get_fit(child2)
                        if fit2 > 0 and child2 not in new_population:
                            new_population[child2] = fit2

                max_possible = 2**self.item_cnt
                min_safe_size = min(max(2, self.__population_cnt // 4), max_possible)
                
                if len(new_population) < min_safe_size:
                    rescue_attempts = 0
                    max_rescue_attempts = 500
                    
                    while len(new_population) < min_safe_size and rescue_attempts < max_rescue_attempts:
                        rescue_attempts += 1
                        random_candidate = rnd.randint(0, 2**self.item_cnt - 1)
                        fit_candidate = self.__get_fit(random_candidate)
                        
                        if fit_candidate > 0 and random_candidate not in new_population:
                            new_population[random_candidate] = fit_candidate
                    
                    if not new_population and self.__population:
                        best_prev = max(self.__population, key=self.__population.get)
                        new_population[best_prev] = self.__population[best_prev]

                if new_population:
                    self.__population = new_population

            if best_solution is None and self.__population:
                valid_final = {k: v for k, v in self.__population.items() if v > 0}
                if valid_final:
                    best_solution = max(valid_final, key=valid_final.get)

            if best_solution is not None:
                mask_str = self.__mask.format(best_solution)
                items = [idx for idx, bit in enumerate(mask_str) if bit == '1']
                cost = self.get_cost([bit == '1' for bit in mask_str])
                return KnapsackSolution(cost=cost, items=items)
            else:
                return KnapsackSolution(cost=0, items=[])
                
        except Exception as e:
            print(f"Error in get_knapsack: {e}")
            import traceback
            traceback.print_exc()
            return KnapsackSolution(cost=0, items=[])

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        population = {}
        max_val = 2**self.item_cnt
        attempts = 0
        max_attempts = population_cnt * 100

        while len(population) < population_cnt and attempts < max_attempts:
            attempts += 1
            item_set = rnd.randint(0, max_val - 1)
            fit = self.__get_fit(item_set)
            if fit > 0 and item_set not in population:
                population[item_set] = fit
        
        while len(population) < population_cnt:
             item_set = rnd.randint(0, max_val - 1)
             if item_set not in population:
                 population[item_set] = self.__get_fit(item_set)

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        if self.item_cnt <= 1:
            return ancestor1, ancestor2

        cross_point = rnd.randint(1, self.item_cnt - 1)
        mask = (1 << self.item_cnt) - 1

        a1_lower = ancestor1 & ((1 << cross_point) - 1)
        a1_upper = ancestor1 >> cross_point
        a2_lower = ancestor2 & ((1 << cross_point) - 1)
        a2_upper = ancestor2 >> cross_point

        child1 = ((a1_upper << cross_point) | a2_lower) & mask
        child2 = ((a2_upper << cross_point) | a1_lower) & mask

        return child1, child2

    def __mutation(self, item_set: int) -> int:
        mutation_rate = 0.1

        for i in range(self.item_cnt):
            if rnd.random() < mutation_rate:
                item_set ^= (1 << i)

        return item_set

    def __get_fit(self, item: int) -> int:
        mask_str = self.__mask.format(item)
        selected = [bit == '1' for bit in mask_str]
        return self.get_cost(selected)

    def __select_parent(self) -> int:
        tournament_size = 3
        actual_tournament_size = min(tournament_size, len(self.__population))
        if actual_tournament_size == 0:
            raise ValueError("Популяция пуста, невозможно выбрать родителя.")
            
        candidates = rnd.sample(
            list(self.__population.keys()),
            actual_tournament_size
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
    
    if result.items:
        total_w = sum(weights[i] for i in result.items)
        print(f"Итоговый вес: {total_w} (Лимит: {weight_limit}) -> {'Валидно' if total_w <= weight_limit else 'Ошибка!'}")
    else:
        print("Решение не найдено (пусто).")
