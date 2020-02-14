import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.lon, self.lat = 37.530887, 55.703118
        self.tip = 'map'
        self.delta = 0.002
        self.params = {"ll": ",".join(list(map(str, [self.lon, self.lat]))),
                       "spn": ",".join(list(map(str, [self.delta, self.delta]))),
                       "l": self.tip}
        self.getImage()
        self.initUI()

    def getImage(self):
        response = requests.get(self.api_server, params=self.params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(self.api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.delta += 0.01
            print('UP!')
        elif event.key() == Qt.Key_PageDown:
            self.delta -= 0.01
            print('DOWN!')
        if event.key() == Qt.Key_Up:
            self.lat += self.delta
        elif event.key() == Qt.Key_Down:
            self.lat -= self.delta
        elif event.key() == Qt.Key_Left:
            self.lon -= self.delta * 4 / 3
        elif event.key() == Qt.Key_Right:
            self.lon += self.delta * 4 / 3
        self.params = {"ll": ",".join(list(map(str, [self.lon, self.lat]))),
                       "spn": ",".join(list(map(str, [self.delta, self.delta]))),
                       "l": self.tip}
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
