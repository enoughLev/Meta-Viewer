import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from Forms.MapForm_ui import Ui_Form
from Workers.YandexStaticApiWorker import YandexMapHandler


class MapWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("MetaViewer")
        self.setWindowIcon(QIcon(self.resource_path("\img\\icon.png")))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.latitude = None
        self.longitude = None
        self.back_btn.clicked.connect(self.open_main_window)

    # Присваивание ширины и долготы
    def set_cords(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    # Отображение карты с указанным масштабом
    def view_map(self, zoom):
        if self.latitude and self.longitude:
            try:
                lat = float(self.latitude)
                lon = float(self.longitude)
            except (TypeError, ValueError):
                return False

            mini_map = YandexMapHandler(lat, lon)
            pixmap = mini_map.view_map(self.map_label.width(), self.map_label.height(), zoom)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.clear()

    # Обработка нажатий клавиатуры
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


    def open_main_window(self):
        self.close()


    # Нужно для корректной работы с файлами в EXE
    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        path = base_path + relative_path
        return path
