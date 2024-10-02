import Plots
from PasswordGenerator import PasswordGenerator
from PasswordHacker import PasswordHacker

def main():
    print("Пункт 1. Визуализация частотного распределения: ")
    pass_len = int(input("Введите длину пароля: "))
    password_generator: PasswordGenerator = PasswordGenerator()
    password_hacker: PasswordHacker = PasswordHacker(password_generator)
    password = password_generator.generate_password(pass_len)
    Plots.create_histogram(password)

    print("Пункт 2. График зависимости времени от длины пароля: ")
    times: list = []
    lens: list = []
    for i in range(1, 5):
        password = password_generator.generate_password(i)
        print("Пароль: " + password)
        hack_time = password_hacker.get_hack_time_of_password(password)
        print("Время подбора: " + str(hack_time))

        lens.append(i)
        times.append(hack_time)

    Plots.create_plot(times, lens)

if __name__ == '__main__':
    main()