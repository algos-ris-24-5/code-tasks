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
        
        population_number = 1
        max_population_number = epoch_cnt
        leader_cnt = 0
        max_leader_cnt = 100
        elite_size = max(1, len(self.__population) // 10)
        
        while population_number < max_population_number and leader_cnt < max_leader_cnt:
            new_population = {}
            sorted_items = sorted(self.__population.keys(), key=lambda k: self.__population[k], reverse=True)
            leader_item = sorted_items[0]
            leader_fit = self.__population[leader_item]
            old_leader_fit = leader_fit
            
            item = rnd.randint(1, 2**self.item_cnt - 1)
            item, fit = self.__get_fit(item)
            new_population[item] = fit
            
            for item in sorted_items[:elite_size]:
                new_population[item] = self.__population[item]
                
            items_to_cross = self.__get_mating_pairs((len(self.__population) - len(new_population))//2)
            
            for item1, item2 in items_to_cross:
                new_item1, new_item2 = self.__cross_items(item1, item2)
                
                if rnd.random() < 0.07:
                    new_item1 = self.__mutate_random(new_item1)
                if rnd.random() < 0.07:
                    new_item2 = self.__mutate_random(new_item2)
                
                new_item1, new_fit1 = self.__get_fit(new_item1)
                new_item2, new_fit2 = self.__get_fit(new_item2)
                
                new_population[new_item1] = new_fit1
                new_population[new_item2] = new_fit2
                
                if new_fit1 > leader_fit:
                    leader_fit = new_fit1
                    leader_item = new_item1
                    leader_cnt = 0
                if new_fit2 > leader_fit:
                    leader_fit = new_fit2
                    leader_cnt = 0
                    leader_item = new_item2
            self.__population = new_population
            population_number+=1
            
            if old_leader_fit == leader_fit:
                leader_cnt += 1

        leader_item = self.__get_bin(leader_item)
        best_items = [i for i, bit in enumerate(leader_item) if bit == '1']
        return KnapsackSolution(cost = leader_fit, items= best_items)

    def __generate_population(self, population_cnt: int) -> dict[int:int]: 
        new_population = {}
        for _ in range(population_cnt):
            item = rnd.randint(1,2**self.item_cnt-1)
            item, fit = self.__get_fit(item)
            new_population[item] = fit
        return new_population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]: # скрестить, посчитать фитнес
        bin_anc1 = self.__get_bin(ancestor1)
        bin_anc2 = self.__get_bin(ancestor2)
        
        point = rnd.randint(1,self.item_cnt-1)
        
        new_item1 = self.__get_ten(bin_anc1[0:point]+bin_anc2[point:])
        new_item2 = self.__get_ten(bin_anc2[0:point]+bin_anc1[point:])
        
        return (new_item1, new_item2)

    def __mutation(self, item_set: int) -> int: 
        
        bin_item = self.__get_bin(item_set)
        gene = rnd.randint(0,self.item_cnt-1)
        
        while bin_item[gene]!='1':
            gene = rnd.randint(0,self.item_cnt-1)
            if '1' not in bin_item:
                return item_set
            
        new_item = ''
        for i in range(self.item_cnt):
            if i!=gene: new_item+=bin_item[i]
            else: new_item+='0'
            
        return self.__get_ten(new_item)
    
    def __get_fit(self, item):
        attempts = 0
        while attempts <= self.item_cnt:   
            
            weight = 0
            bin_item = self.__get_bin(item)
            
            for i in range(self.item_cnt):
                weight += int(bin_item[i]) * self.weights[i]
            
            if weight <= self.weight_limit:
                fit = sum(int(bin_item[i]) * self.costs[i] for i in range(self.item_cnt))
                return item, fit
            else:
                item = self.__mutation(item)
            attempts += 1

        return item, 0

    def __get_bin(self, value):
        return self.__mask.format(value)
    
    def __get_ten(self, value):
        return int(value,2)
        
    def __tournament_select(self, tournament_size: int = 3) -> int:
        
        population_keys = list(self.__population.keys())
        
        k = min(tournament_size, len(population_keys))
        competitors = rnd.sample(population_keys, k=k)
        
        winner_key = max(competitors, key=lambda k: self.__population[k])
        
        return winner_key

    def __get_mating_pairs(self, num_pairs: int) -> list[tuple[int, int]]:
        
        pairs = []
        for _ in range(num_pairs):
            parent1 = self.__tournament_select()
            parent2 = self.__tournament_select()
            attempts = 0
            while parent2 == parent1 and attempts < 5:
                parent2 = self.__tournament_select()
                attempts += 1
            pairs.append((parent1, parent2))
        return pairs
    
    def __mutate_random(self, item: int) -> int:
        bin_item = list(self.__get_bin(item))
        gene = rnd.randint(0, self.item_cnt - 1)
        bin_item[gene] = '1' if bin_item[gene] == '0' else '0'
        return self.__get_ten(''.join(bin_item))

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
