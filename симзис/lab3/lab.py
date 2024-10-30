import sympy
import math

# Быстрое возведение в степень по модулю с помощью метода повторяющихся возведений в квадрат
def modular_exponentiation(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result

# Проверка, является ли g первообразным корнем по модулю P
def is_primitive_root(g, P):
    required_set = set(range(1, P))
    actual_set = set(modular_exponentiation(g, powers, P) for powers in range(1, P))
    return required_set == actual_set

# Поиск первообразного корня по модулю P
def find_primitive_root(P):
    for g in range(2, P):
        if is_primitive_root(g, P):
            return g
    return None




try:
    P = 7759
    print("Простое число P: 7759")
    a = int(input("Введите секретное число Алисы (a): "))
    b = int(input("Введите секретное число Боба (b): "))

    
    if not sympy.isprime(P):
        raise ValueError("Число P должно быть простым.")

    g = find_primitive_root(P)
    if g is None:
        raise ValueError("Не удалось найти первообразный корень для данного числа P.")

    print(f"Найденный первообразный корень g по модулю {P}: {g}")

    A = pow(g, a, P) # Алиса вычисляет g^a mod P и отправляет Бобу
    B = pow(g, b, P) # Боб вычисляет g^b mod P и отправляет Алисе
    secret_A = pow(B, a, P)  # B^a mod P
    secret_B = pow(A, b, P)  # A^b mod P

    if secret_A == secret_B:
        print(f"Общий секретный ключ, полученный Алисой и Бобом: {secret_A}")
    else:
        print("Ошибка: общий секрет не совпадает.")  
    
    key_length_bits = math.floor(math.log2(P)) + 1
    print(f"Оценочная длина секретного ключа в битах: {key_length_bits} бит")

    # Атака "Человек посередине"
    a_joe = int(input("Введите секретное число Джо для Алисы (a_joe): "))
    b_joe = int(input("Введите секретное число Джо для Боба (b_joe): "))


    A = modular_exponentiation(g, a, P)
    print(f"Алиса отправляет A: {A}")
    A_joe = modular_exponentiation(g, a_joe, P)
    print(f"Джо отправляет Бобу A_joe: {A_joe}") # Джо перехватывает A, заменяет его на свой, отправляет Бобу


    B = modular_exponentiation(g, b, P)
    print(f"Боб отправляет B: {B}")
    B_joe = modular_exponentiation(g, b_joe, P)
    print(f"Джо отправляет Алисе B_joe: {B_joe}") # Джо перехватывает B, заменяет его на свой, отправляет Алисе


    secret_Alice_Joe = modular_exponentiation(B_joe, a, P)  # B_joe^a mod P
    print(f"Общий секретный ключ между Алисой и Джо: {secret_Alice_Joe}")
    secret_Bob_Joe = modular_exponentiation(A_joe, b, P)    # A_joe^b mod P
    print(f"Общий секретный ключ между Бобом и Джо: {secret_Bob_Joe}")

except ValueError as e:
    print(e)
