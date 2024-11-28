import random


#проверка простое ли число
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1


    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

#генерация простого числа 1024битного
def generate_large_prime(bits=1024):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

#нод
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#страшни мультипликативни алгоритм евклида...
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def generate_keypair(bits=1024):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    fi = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, fi) != 1:
        e = random.randrange(2, fi)

    d = modinv(e, fi)

    return (e, n), (d, n)


def modular_exponentiation(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result



def encrypt(message, pubkey):
    e, n = pubkey
    return modular_exponentiation(message, e, n)


def decrypt(ciphertext, privkey):
    d, n = privkey
    return modular_exponentiation(ciphertext, d, n)


def sign(message, privkey):
    d, n = privkey
    return modular_exponentiation(message, d, n)


def verify(message, signature, pubkey):
    e, n = pubkey
    return message == modular_exponentiation(signature, e, n)


def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(str(data))


def read_from_file(filename):
    with open(filename, 'r') as file:
        return int(file.read().strip())


#tестирование системы RSA на 10 сообщениях
def test_rsa():
    pubkey, privkey = generate_keypair()

    write_to_file("public_key.txt", pubkey)
    write_to_file("private_key.txt", privkey)

    print(f"Открытый ключ (e, n): {pubkey}")
    print(f"Закрытый ключ (d, n): {privkey}\n")

    for i in range(10):
        print(f"Тест {i + 1}")

        message = random.randint(0, pubkey[1] - 1)
        write_to_file(f"message_{i + 1}.txt", message)

        ciphertext = encrypt(message, pubkey)
        write_to_file(f"encrypted_message_{i + 1}.txt", ciphertext)

        decrypted_message = decrypt(ciphertext, privkey)

        signature = sign(message, privkey)
        write_to_file(f"signature_{i + 1}.txt", signature)

        is_valid_signature = verify(message, signature, pubkey)

        print(f"Сообщение: {message}")
        print(f"Зашифрованное сообщение: {ciphertext}")
        print(f"Расшифрованное сообщение: {decrypted_message}")
        print(f"Подпись: {signature}")
        print(f"Проверка подписи: {'успешно' if is_valid_signature else 'неудачно'}\n")

        assert decrypted_message == message, f"Ошибка: не удалось расшифровать сообщение {i + 1}!"
        assert is_valid_signature, f"Ошибка: не удалось проверить подпись для сообщения {i + 1}!"

        print(f"Тест {i + 1} пройден успешно.\n")

    print("10 тестов для шифрования, расшифровки и цифровой подписи успешно пройдены.")


test_rsa()
