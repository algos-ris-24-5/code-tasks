def gcd_recursive (a,b):
    a, b = abs(a), abs(b)
    if b == 0:
        return a
    return gcd_recursive(b, a % b)

def gcd_iterative_slow(a,b):
    a, b = abs(a), abs(b)
    while a != 0 and b != 0:
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
    a, b = abs(a), abs(b)
    while b!=0:
        temp = b
        b = a % b
        a = temp
    return a

def lcm(a, b):
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
