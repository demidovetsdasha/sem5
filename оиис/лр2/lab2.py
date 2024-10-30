import cv2
import numpy as np
from matplotlib import pyplot as plt


def show_images(original, filtered, title):
    plt.figure(figsize=(10, 5))

    # оригинальное изображение
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title('Оригинальное изображение')
    plt.axis('off')

    # обработанное изображение
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')

    plt.show()


def apply_filters(image_path):
    img = cv2.imread(image_path)

    # 1. Медианный фильтр
    median_filtered = cv2.medianBlur(img, 15)
    show_images(img, median_filtered, 'Медианный фильтр')

    # 2. Обычное размытие (Blur)
    blur_filtered = cv2.blur(img, (15, 15))
    show_images(img, blur_filtered, 'Обычное размытие')

    # 3. Гауссово размытие
    gaussian_filtered = cv2.GaussianBlur(img, (15, 15), 0)
    show_images(img, gaussian_filtered, 'Гауссово размытие')

    # 4. Двусторонний фильтр (сильное размытие)
    bilateral_filtered = cv2.bilateralFilter(img, 15, 150, 150)
    show_images(img, bilateral_filtered, 'Двусторонний фильтр (сильное размытие)')

    # 5. Фильтр Собеля
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    sobel_combined = cv2.magnitude(sobelx, sobely)
    sobel_combined = cv2.convertScaleAbs(sobel_combined)  # Приведение к диапазону [0, 255]
    sobel_highlighted = cv2.addWeighted(img, 0.6, sobel_combined, 0.4, 0)

    show_images(img, sobel_highlighted, 'Фильтр Собеля')



image_path = 'scale_1200.jpg'
apply_filters(image_path)
