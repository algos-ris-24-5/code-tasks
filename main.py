STR_LENGTH_ERROR_MSG = "Длина строки должна быть целым положительным числом"
"""Сообщение об ошибке при некорректном значении параметра Длина строки"""

NOT_INT_VALUE_TEMPL = "Параметр {0} Не является целым числом"
"""Шаблон сообщения об ошибке при нечисловом значении параметра"""

NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
"""Шаблон сообщения об ошибке при отрицательном значении параметра"""

N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"
"""Сообщение об ошибке при значении параметра n меньше чем k"""

def generation_booles(length: int) -> list[str]:
    if length == 0: return []
    if length == 1: return ['0']
    return [s + '0' for s in generation_ones(length - 1)]

def generation_ones(length: int) -> list[str]:
    if length == 0: return []
    if length == 1: return ['1']
    return [s + '1' for s in generation_booles(length - 1) + generation_ones(length - 1)]

def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: Длина строки.
    :raise ValueError: Если длина строки не является целым положительным
    числом.
    :return: Список строк.
    """
    if not isinstance(length, int) or length <= 0: raise ValueError(STR_LENGTH_ERROR_MSG)
    if isinstance(length, bool): raise ValueError(STR_LENGTH_ERROR_MSG)
    return sorted(generation_booles(length) + generation_ones(length))
        


def binomial_coefficient(n: int, k: int, use_rec=False) -> int:
    """Вычисляет биномиальный коэффициент из n по k.
    :param n: Количество элементов в множестве, из которого производится выбор.
    :param k: Количество элементов, которые нужно выбрать.
    :param use_rec: Использовать итеративную или рекурсивную реализацию функции.
    :raise ValueError: Если параметры не являются целыми неотрицательными
    числами или значение параметра n меньше чем k.
    :return: Значение биномиального коэффициента.
    """
    
    if not isinstance(n, int) :
        raise ValueError(NOT_INT_VALUE_TEMPL.format("n"))
    
    if not isinstance(k,int):
        raise ValueError(NOT_INT_VALUE_TEMPL.format("k"))
    
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    
    if n<k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)
    
    
    if use_rec:
        if n==1 or n==k or k==0:
            return 1
        if k==1:
            return n
        return binomial_coefficient(n-1, k, True) + binomial_coefficient(n-1, k-1, True)
    else:
        k = min(k, n-k)
        result = [[0 for i in range(n+1)] for i in range(k+1)]
        result[0] = [1 for i in range(n+1)]
        for i in range(1,k+1):
            for j in range(0, n):
                result[i][j] = result[i][j-1] + result[i-1][j-1]
        
        return result[k][n-1]



def main():
    n = 2
    print(f"Строки длиной {n}:\n{generate_strings(n)}")

    n = 30
    k = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k),
    )
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ",
        binomial_coefficient(n, k, use_rec=True),
    )


if __name__ == "__main__":
    main()
