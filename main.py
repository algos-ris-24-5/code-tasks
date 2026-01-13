from collections import namedtuple

from strenum import StrEnum


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках."""

    WRONG_MATRIX = (
        "Таблица прибыли от проектов не является прямоугольной "
        "матрицей с числовыми значениями"
    )
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distribution"])


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)

def matrix_validation(profit_matrix: list[list[int]]) -> None:
    """
    Функция валидации матрицы
    """
    
    # None вместо матрицы
    if profit_matrix == None:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    # Пустая матрица
    if len(profit_matrix) == 0:
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    
    # Пустой ряд матрицы
    if (len(profit_matrix[0]) == 0):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    # Матрица прибыли не является прямоугольной и хотя бы одно значение не является числом
    for i in range(len(profit_matrix)):

        # Проверка если матрица прибыли не является прямоугольной
        if i != 0 and len(profit_matrix[i-1]) != len(profit_matrix[i]):
            raise ValueError(ErrorMessages.WRONG_MATRIX)

        for j in range(len(profit_matrix[i])):
            #Проверка чтобы все значения были числами
            if not isinstance(profit_matrix[i][j], int):
                raise ValueError(ErrorMessages.WRONG_MATRIX)
            
            # Проверка отрицательных значений
            if profit_matrix[i][j] < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, j, i)
            
            # Проверка на неубывание прибыли при увеличении инвестиций
            if i != 0 and profit_matrix[i][j] < profit_matrix[i-1][j]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, j, i)

def get_invest_distribution(
    profit_matrix: list[list[int]],
) -> Result:
    """Рассчитывает максимально возможную прибыль и распределение инвестиций
    между несколькими проектами. Инвестиции распределяются кратными частями.

    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    :return: именованный кортеж Result с полями:
    profit - максимально возможная прибыль от инвестиций,
    distribution - распределение инвестиций между проектами.
    """

    matrix_validation(profit_matrix)

    profit = [[0 for j in range(len(profit_matrix[0]) + 1)] for _ in range(len(profit_matrix) + 1)]
    distributions = [[0 for j in range(len(profit_matrix[0]) + 1)] for _ in range(len(profit_matrix) + 1)]

    for project in range(1, len(profit_matrix[0]) + 1):
        for investment in range(len(profit_matrix) + 1):
            for current_investment in range(investment + 1):
                if current_investment == 0:
                    current_project_profit = 0
                else: 
                    current_project_profit = profit_matrix[current_investment - 1][project - 1]
                
                previous_project_investment = profit[investment - current_investment][project - 1]

                current_profit = current_project_profit + previous_project_investment
                if current_profit >= profit[investment][project]:
                    profit[investment][project] = current_profit
                    distributions[investment][project] = current_investment

    max_profit = profit[len(profit_matrix)][len(profit_matrix[0])]
    distribution = [0] * len(profit_matrix[0])

    current_investments = len(profit_matrix)

    for project in range(len(profit_matrix[0]), 0, -1):
        distribution[project - 1] = distributions[current_investments][project]
        current_investments -= distributions[current_investments][project]
    
    return Result(profit=max_profit, distribution=distribution)

def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]

    print(get_invest_distribution(profit_matrix))


if __name__ == "__main__":
    main()
