from ultralytics import YOLO
import cv2


def detect_object(image_path: str, target_object: str):
    model = YOLO('yolov5su.pt')

    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return

    results = model(image, verbose=False)

    classes = results[0].boxes.cls.cpu().numpy()
    names = results[0].names

    detected_objects = [names[int(cls)] for cls in classes]

    count = 0

    for detected in detected_objects:
        if target_object.lower() in detected.lower():
            count += 1

    if count > 0:
        print(f"Объект '{target_object}' найден на изображении! Количество: {count}")

    annotated_image = results[0].plot()
    cv2.imshow("Распознанные объекты", annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



image_path = "D:/Мои проекты/сем5/ОИИС/лабы мои/Lab6 IZO/test.jpg" 
target_object = input("Введите название объекта для поиска (на английском): ")
detect_object(image_path, target_object)
