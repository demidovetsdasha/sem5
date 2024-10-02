import matplotlib.pyplot as plt
import numpy as np


def count_chars(text: str):
    char_count = [0] * 128
    for char in text:
        if ord(char) < 128:
            char_count[ord(char)] += 1
    return char_count


def create_histogram(password: str):
    char_count = count_chars(password)
    plt.figure(figsize=(12, 6))
    plt.bar(range(128), char_count, width=1)
    plt.title('Распределение символов в строке')
    plt.xlabel('ASCII код')
    plt.ylabel('Частота появления')
    plt.xticks(range(0, 144, 16))
    plt.tight_layout()
    plt.show()


def create_plot(time_array, length_array):
    plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(111)
    ax1.plot(time_array, length_array, 'bo-', markersize=8, label='Длина пароля')
    ax1.set_xlabel('Время выполнения (сек)')
    ax1.set_ylabel('Длина пароля', color='b')
    lines1 = ax1.get_lines()
    ax1.legend(lines1, "Длина пароля", loc='upper left')
    plt.xticks(rotation=45)
    plt.title("Длина пароля в зависимости от времени выполнения")
    plt.tight_layout()
    plt.show()
