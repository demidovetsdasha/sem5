import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox
import matplotlib.pyplot as plt

def load_image(title="Выберите изображение"):
    Tk().withdraw()  
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Images", "*.jpg *.jpeg *.png")])
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {file_path}")
        return img
    else:
        messagebox.showinfo("Информация", "Файл не выбран.")
        return None


def create_anaglyph(left_image, right_image, method):
    h, w = left_image.shape[:2]
    right_image = cv2.resize(right_image, (w, h))

    left_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    if method == "Color Anaglyph":
        anaglyph = np.zeros_like(left_image)
        anaglyph[:, :, 0] = left_gray  # красный из левого
        anaglyph[:, :, 1] = right_image[:, :, 1]  # зелёный из правого
        anaglyph[:, :, 2] = right_image[:, :, 2]  # синий из правого
    elif method == "Half Color Anaglyph":
        anaglyph = np.zeros_like(left_image)
        anaglyph[:, :, 0] = left_gray  # красный из левого
        anaglyph[:, :, 1] = cv2.multiply(right_gray, 0.5).astype(np.uint8)  # полутона зелёного из правого
        anaglyph[:, :, 2] = cv2.multiply(right_gray, 0.5).astype(np.uint8)  # полутона синего из правого
    elif method == "Optimized Anaglyph":
        anaglyph = np.zeros_like(left_image)
        anaglyph[:, :, 0] = left_gray  # красный из левого
        anaglyph[:, :, 1] = cv2.multiply(right_image[:, :, 1], 0.7).astype(np.uint8)  # оптимизированный зелёный
        anaglyph[:, :, 2] = cv2.multiply(right_image[:, :, 2], 0.7).astype(np.uint8)  # оптимизированный синий
    else:
        raise ValueError(f"Метод '{method}' не поддерживается.")

    return anaglyph


def show_anaglyph(anaglyph, method_name):
    plt.imshow(cv2.cvtColor(anaglyph, cv2.COLOR_BGR2RGB))
    plt.title(f"Метод: {method_name}")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    print("Выберите изображение для левого глаза.")
    left_img = load_image("Выберите изображение для левого глаза")
    if left_img is None:
        print("Левое изображение не выбрано. Завершение программы.")
        exit()

    print("Выберите изображение для правого глаза.")
    right_img = load_image("Выберите изображение для правого глаза")
    if right_img is None:
        print("Правое изображение не выбрано. Завершение программы.")
        exit()

    methods = ["Color Anaglyph", "Half Color Anaglyph", "Optimized Anaglyph"]

    for method in methods:
        print(f"Создание анаглифа методом: {method}")
        try:
            anaglyph = create_anaglyph(left_img, right_img, method)
            show_anaglyph(anaglyph, method)
        except Exception as e:
            print(f"Ошибка при создании анаглифа методом '{method}': {e}")
