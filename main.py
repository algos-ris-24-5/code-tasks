from collections import namedtuple

from srtenum import StrEnum


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
    # Валидация структуры матрицы
    if not profit_matrix or not isinstance(profit_matrix, list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    rows_count = len(profit_matrix)
    
    # Проверка на список списков и пустоту первой строки
    if not rows_count or not isinstance(profit_matrix[0], list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    cols_count = len(profit_matrix[0])
    if cols_count == 0:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    # Валидация типов данных и прямоугольности
    for r_idx, row in enumerate(profit_matrix):
        if not isinstance(row, list) or len(row) != cols_count:
            raise ValueError(ErrorMessages.WRONG_MATRIX)
        
        for c_idx, val in enumerate(row):
            if not isinstance(val, (int, float)):
                raise ValueError(ErrorMessages.WRONG_MATRIX)
            
            # Проверка на отрицательную прибыль
            if val < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, c_idx, r_idx)
            
            # Проверка на неубывание прибыли
            if r_idx > 0:
                prev_val = profit_matrix[r_idx - 1][c_idx]
                if val < prev_val:
                    raise ProfitValueError(ErrorMessages.DECR_PROFIT, c_idx, r_idx)

    # Динамическое программирование
    max_steps = rows_count
    dp = [[0] * (max_steps + 1) for i in range(cols_count)]

    # Инициализация первого проекта (индекс 0)
    for s in range(1, max_steps + 1):
        dp[0][s] = profit_matrix[s - 1][0]

    # Заполнение таблицы для остальных проектов
    for p in range(1, cols_count):
        for s in range(1, max_steps + 1):
            max_p = 0
            # Перебираем варианты: k шагов в текущий проект p, 
            for k in range(s + 1):
                current_project_profit = 0 if k == 0 else profit_matrix[k - 1][p]
                prev_projects_profit = dp[p - 1][s - k]
                total_profit = current_project_profit + prev_projects_profit
                
                if total_profit > max_p:
                    max_p = total_profit
            
            dp[p][s] = max_p

    max_total_profit = dp[cols_count - 1][max_steps]

    # Восстановление пути
    distribution = [0] * cols_count
    remaining_steps = max_steps

    # Идем от последнего проекта к первому
    for p in range(cols_count - 1, 0, -1):
        for k in range(remaining_steps + 1):
            curr_prof = 0 if k == 0 else profit_matrix[k - 1][p]
            prev_prof = dp[p - 1][remaining_steps - k]
            
            if curr_prof + prev_prof == dp[p][remaining_steps]:
                distribution[p] = k
                remaining_steps -= k
                break
    
    distribution[0] = remaining_steps

    return Result(max_total_profit, distribution)


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
