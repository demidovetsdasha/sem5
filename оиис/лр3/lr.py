import cv2
import numpy as np
import matplotlib.pyplot as plt


def equalize_brightness(image):
    # перевод в цветовое пространство YCrCb 
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)

    # адаптивное выравнивание гистограммы
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    y_equalized = clahe.apply(y)

    # объединение каналов и перевод обратно в BGR
    ycrcb_equalized = cv2.merge((y_equalized, cr, cb))
    image_equalized = cv2.cvtColor(ycrcb_equalized, cv2.COLOR_YCrCb2BGR)

    return image_equalized


image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpeg')

image1_equalized = equalize_brightness(image1)
image2_equalized = equalize_brightness(image2)

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.title("Оригинальное изображение")
plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 2)
plt.title("Обработанное изображение")
plt.imshow(cv2.cvtColor(image1_equalized, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 3)
plt.title("Оригинальное изображение")
plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 4)
plt.title("Обработанное изображение")
plt.imshow(cv2.cvtColor(image2_equalized, cv2.COLOR_BGR2RGB))

plt.show()