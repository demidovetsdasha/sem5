import numpy as np
import matplotlib.pyplot as plt
import cmath


# Функция для генерации синусоидального сигнала
def generate_sine_wave(freq, sampling_rate, duration):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * freq * t)
    return t, signal


# Функция для дополнения сигнала до ближайшей длины, являющейся степенью двойки
def pad_to_power_of_two(signal):
    N = len(signal)
    next_pow_of_2 = 2 ** int(np.ceil(np.log2(N)))
    padded_signal = np.pad(signal, (0, next_pow_of_2 - N), 'constant')
    return padded_signal


# Собственная реализация БПФ (рекурсивная)
def fft(signal):
    N = len(signal)
    if N <= 1:
        return signal

    # Разделение на четные и нечетные индексы
    even = fft(signal[0::2])
    odd = fft(signal[1::2])

    T = [cmath.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]

    return [even[k] + T[k] for k in range(N // 2)] + \
        [even[k] - T[k] for k in range(N // 2)]


# Визуализация результатов БПФ
def plot_fft(signal, sampling_rate):
    # Дополнение сигнала до длины, кратной степени двойки
    padded_signal = pad_to_power_of_two(signal)

    # Применение собственного БПФ
    fft_result = fft(padded_signal)

    # Частоты
    freqs = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)

    # Амплитуды (модуль комплексного числа)
    fft_magnitude = np.abs(fft_result)

    # Отображаем только положительные частоты (первая половина спектра)
    half_len = len(freqs) // 2

    plt.figure(figsize=(12, 6))

    # Временная область
    plt.subplot(1, 2, 1)
    plt.plot(signal)
    plt.title('Сигнал во временной области')
    plt.xlabel('Время (сэмплы)')
    plt.ylabel('Амплитуда')

    # Частотная область (после БПФ)
    plt.subplot(1, 2, 2)
    plt.plot(freqs[:half_len], fft_magnitude[:half_len])
    plt.title('Спектр частот (БПФ)')
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')

    plt.tight_layout()
    plt.show()


# Основная функция
def main():
    # Параметры
    freq = float(input("Введите частоту синусоиды (Гц): "))  # Частота синусоиды
    sampling_rate = 1000  # Частота дискретизации (Гц)
    duration = 0.1  # Длительность сигнала (секунды)

    # Генерация сигнала
    t, signal = generate_sine_wave(freq, sampling_rate, duration)

    # Отображение графиков
    plot_fft(signal, sampling_rate)


# Запуск программы
if __name__ == "__main__":
    main()
