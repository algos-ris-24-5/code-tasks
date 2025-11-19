import time


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
<<<<<<< HEAD
    a = abs(a)
    b=abs(b)
    if b==0: return a
    return gcd_recursive(b,a%b)
=======
    pass
>>>>>>> cdfb8a00730ee70268bab5e0b2d3a83e3a7e9f6b


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
<<<<<<< HEAD
    a = abs(a)
    b=abs(b)
    while a!=b:
        if a>b: a-=b
        else: b-=a
    return a
=======
    pass
>>>>>>> cdfb8a00730ee70268bab5e0b2d3a83e3a7e9f6b


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
<<<<<<< HEAD
    a = abs(a)
    b=abs(b)
    temp = 0
    while a!=0:
        temp = b%a
        b = a
        a = temp
    return b
=======
    pass
>>>>>>> cdfb8a00730ee70268bab5e0b2d3a83e3a7e9f6b


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :return: значение наименьшего общего кратного
    """
<<<<<<< HEAD
    return int(a*b/gcd_iterative_fast(a,b))
=======
    pass
>>>>>>> cdfb8a00730ee70268bab5e0b2d3a83e3a7e9f6b


def main():
    a = 1005002
    b = 1354
    print(f"Вычисление НОД чисел {a} и {b} рекурсивно:")
    start_time = time.time()
    print(gcd_recursive(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с вычитанием:")
    start_time = time.time()
    print(gcd_iterative_slow(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с делением:")
    start_time = time.time()
    print(gcd_iterative_fast(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОК чисел {a} и {b}:")
    start_time = time.time()
    print(lcm(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> cdfb8a00730ee70268bab5e0b2d3a83e3a7e9f6b
