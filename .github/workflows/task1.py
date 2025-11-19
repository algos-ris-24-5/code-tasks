def gcd_recursive (a,b):
    # База
    if b == 0:
        return a
    # Рекурсивно вызываем функцию с аргументами b и остатком от деления a на b
    return gcd_recursive(b, a % b)

def gcd_iterative_slow(a,b):
    # Заглушка
    while a != 0 and b != 0:
        # Вычитаем из большего числа меньшее
        if a > b:
            a = a - b
        else:
            b = b - a
    if a!=0:
        x = a
    if b!=0:
        x=b
    return x

def gcd_iterative_fast(a, b):
       # Заглушка5
        while b!=0:

        # Сохраняем текущее значение b
            temp = b
            # Обновляем b как остаток от деления a на b
            b = a % b
            # Обновляем a как предыдущее значение b
            a = temp
        return a

def lcm(a, b):
    # Используем формулу: НОК(a, b) = (a * b) / НОД(a, b)
    # Для избежания переполнения сначала делим a на НОД
    return a // gcd_iterative_fast(a, b) * b

if __name__ == "__main__":
    print("Введите 2 числа через enter")
    num1 = int(input())
    num2 = int(input())
    
    print(f"Числа: {num1} и {num2}")
    print(f"НОД рекурсивный: {gcd_recursive(num1, num2)}")
    print(f"НОД итерационный (вычитание): {gcd_iterative_slow(num1, num2)}")
    print(f"НОД итерационный (деление): {gcd_iterative_fast(num1, num2)}")
    print(f"НОК: {lcm(num1, num2)}")