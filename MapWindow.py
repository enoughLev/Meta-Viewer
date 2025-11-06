from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from Forms.MapForm_ui import Ui_Form
from YandexStaticApiWorker import YandexMapHandler
#import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class MapWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.latitude = None
        self.longitude = None

        self.back_btn.clicked.connect(self.open_main_window)


    def set_cords(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def open_main_window(self):
        self.close()