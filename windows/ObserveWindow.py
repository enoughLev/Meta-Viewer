import os
import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform, QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QTableWidgetItem

from GaleryWindow import GalleryWindow
from MapWindow import MapWindow
from Forms.ObserveForm_ui import Ui_MainWindow


from workers.ImageViewWoker import ImageViewer
from workers.MetadataWorker import ImageMetadataExtractor
from workers.DatabaseWorker import MetadataDatabase
from workers.YandexStaticApiWorker import YandexMapHandler

class ObserverWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Настройка формы
        self.setupUi(self)
        self.setWindowTitle("Главное окно")
        self.setWindowIcon(QIcon(self.resource_path("\img\\icon.png")))

        # Объявление переменных
        self.map_form = None
        self.record = None
        self.dict_meta = None

        self.db = MetadataDatabase(self.resource_path("\Database\MetaViewerDB.db"))
        #self.db = MetadataDatabase("Database/MetaViewerDB.db")
        self.file_path = [self.resource_path("\img\\hello.png"), "Static IMG"]

        # Создание дополнительных объектов
        self.gallery_form = GalleryWindow()
        self.image_viewer = ImageViewer()

        # Настройка элементов формы
        self.layout.addWidget(self.image_viewer)
        self.metadata_table.setHorizontalHeaderLabels(["", ""])
        self.metadata_table.setStyleSheet("background-color: #f0f0f0;")
        self.metadata_table.setColumnWidth(0, 170)
        self.metadata_table.setColumnWidth(1, 330)
        self.rotate_btn.setIcon(QIcon(self.resource_path("\img\\rotate.png")))
        self.image_viewer.setImage(self.file_path[0])

        # Привязка действий к кнопкам
        self.open_gallery_btn.clicked.connect(self.open_gallery)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.rotate_btn.clicked.connect(self.image_viewer.rotate_clockwise_90)
        self.exit_btn.clicked.connect(self.close)
        self.map_label.mousePressEvent = self.handle_map_label_click


    def handle_map_label_click(self, event):
        self.open_full_size_map()

    def open_full_size_map(self):
        try:
            if self.dict_meta["Latitude"] and self.dict_meta["Longitude"]:
                self.map_form = MapWindow()
                self.map_form.set_cords(self.dict_meta["Latitude"], self.dict_meta["Longitude"])
                self.map_form.view_map(16)
                self.map_form.show()

        except Exception as e:
            print(f"Ошибка при открытии карты: {e}")


    def view_map(self, zoom):
        if self.dict_meta["Latitude"] and self.dict_meta["Longitude"]:
            try:
                lat = float(self.dict_meta.get("Latitude"))
                lon = float(self.dict_meta.get("Longitude"))
            except (TypeError, ValueError):
                return False

            mini_map = YandexMapHandler(lat, lon)
            pixmap = mini_map.view_map(self.map_label.width(), self.map_label.height(), zoom)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.clear()


    def open_gallery(self):
        self.gallery_form.show()

    def choose_file(self):
        try:
            print("\nНОВЫЙ ВЫВОД:")
            self.file_path = QFileDialog.getOpenFileName(self, 'Выбор файла', "C:\\Users\levch\Downloads\Phone Link", 'Изображения (*.png *.jpg *.jpeg)')
            if not self.file_path:
                print("Файл не выбран.")
                return

            self.image_viewer.setImage(self.file_path[0])

            if self.file_path[0].lower().endswith("jpeg"):
                self.image_viewer.rotate_clockwise_90()

            self.catch_metadata()
            self.insert_to_database()
            self.filling_table()
            self.view_map(13) # Указываем увеличение, default = 13

        except Exception as e:
            print(f"Ошибка при выборе или обработке файла: {e}")


    def catch_metadata(self):
        metadata = ImageMetadataExtractor(self.file_path[0])
        self.dict_meta = metadata.get_metadata_dict()
        print("Caught metadata in dictionary (for insert into DataBase):\n\t", self.dict_meta)

    def insert_to_database(self):
        try:
            self.db.connect()
            self.db.insert_metadata(self.dict_meta)
            self.db.insert_image(self.file_path[0])
            self.db.close()

        except Exception as e:
            print(f"Ошибка при добавлении в базу данных: {e}")


    def filling_table(self):
        keys_order = [
            "NameFile","Make", "Model", "Software", "DateTime",
            "HostComputer", "Mode", "Flash", "ColorSpace",
            "ExifImageWidth", "ExifImageHeight", "OffsetTime",
            "Latitude", "Longitude"
        ]

        if self.dict_meta is None:
            row_count = self.metadata_table.rowCount()
            for row in range(row_count):
                self.metadata_table.setItem(row, 1, QTableWidgetItem(""))
            return

        for row, key in enumerate(keys_order):
            val = self.dict_meta.get(key, "") if self.dict_meta.get(key) is not None else ""
            self.metadata_table.setItem(row, 1, QTableWidgetItem(str(val)))

    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            files = os.listdir(base_path)
            for filename in files:
                print(filename)
        else:
            base_path = os.path.abspath(".")

        path = base_path + relative_path
        return path

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.open_full_size_map()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


