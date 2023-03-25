# Импорт
import cv2
import numpy as np

# Функция добавления шума на фото
def noise():
    # Загружаем картинку
    img = cv2.imread(r'C:\Users\--\Desktop\Variant5.jpg', cv2.IMREAD_COLOR)

    # Создаем два массива - значения пикселей и случайные значения
    image = np.array(img/255, dtype=float)
    noise = np.random.normal(0, 0.15, img.shape)

    # Складываем массивы, чтобы получить эффект шума
    out = image + noise

    # Вывод изображения
    cv2.imshow('test', out)
    cv2.waitKey(0)


def tracking():

    # Загружаем видео
    cap = cv2.VideoCapture(r'C:\Users\--\Desktop\target.mp4')

    # Задаем детектор, отделяющий объект от фона
    detector = cv2.createBackgroundSubtractorMOG2(history=100)

    # Цикл вывода видео покадрово
    while True:

        # Берем кадр
        ret, frame = cap.read()

        # Применяем к нему маску(детектор) так, что бы на маске отображались только белые пиксели
        mask = detector.apply(frame)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

        # Ищем контур объекта
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Здесь рисуем обводку
        for cnt in contours:
            # Добавлено ограничение на контур, чтобы исключить ложные срабатывания
            area = cv2.contourArea(cnt)
            if area > 400:
                (x,y), r =cv2.minEnclosingCircle(cnt)
                center =(int(x),int(y))
                r = int(r)
                if center[0] < 215 and center[1] < 120:
                    cv2.circle(frame, center, r, (255, 0, 0), 5)
                elif center[0] > 640 and center[1] > 360:
                    cv2.circle(frame, center, r, (0, 0, 255), 5)
                else:
                    cv2.circle(frame, center, r, (100, 100, 100), 3)

        # Вывод
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



var = int(input("""Введите 1 для наложения шума на картинку
Введите 2 для отслеживания метки на видео\n"""))

match var:
    case 1:
        noise()
    case 2:
        tracking()


