import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem

from Windows.GalleryWindow import GalleryWindow
from Windows.MapWindow import MapWindow


from Workers.ImageViewWoker import ImageViewer

from Workers.MetadataWorker import ImageMetadataExtractor
from Workers.DatabaseWorker import MetadataDatabase
from Workers.YandexStaticApiWorker import YandexMapHandler

from Forms.ObserveForm_ui import Ui_MainWindow


class ObserverWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Настройка формы
        self.setupUi(self)
        self.setWindowTitle("MetaViewer")
        self.setWindowIcon(QIcon(self.resource_path("\img\\icon.png")))
        self.setFixedSize(1200, 775)
        # Объявление переменных
        self.map_form = None
        self.record = None
        self.dict_meta = None

        self.db = MetadataDatabase(self.resource_path("\Database\MetaViewerDB.db"))
        self.file_path = [self.resource_path("\img\\hello.png"), "Static IMG"]

        # Создание дополнительных объектов
        self.gallery_form = GalleryWindow()
        self.gallery_form.imageSelected.connect(self.handle_gallery_image_selected)
        self.image_viewer = ImageViewer()

        # Настройка элементов формы
        self.layout.addWidget(self.image_viewer)
        self.metadata_table.setHorizontalHeaderLabels(["", ""])
        self.metadata_table.setStyleSheet("background-color: #f0f0f0;")
        self.metadata_table.setColumnWidth(0, 170)
        self.metadata_table.setColumnWidth(1, 330)
        self.rotate_btn.setIcon(QIcon(self.resource_path("\img\\rotate.png")))
        self.image_viewer.setImageFromPath(self.file_path[0])

        # Привязка действий к кнопкам
        self.open_gallery_btn.clicked.connect(self.open_gallery)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.rotate_btn.clicked.connect(self.image_viewer.rotate_clockwise_90)
        self.exit_btn.clicked.connect(self.close)
        self.map_label.mousePressEvent = self.handle_map_label_click

    # Функция для открытия полномасштабной карты по нажатию на картинку мини-карты
    def handle_map_label_click(self, event):
        self.open_full_size_map()

    # Функция для открытия окна с полномасштабной картой и передачей в форму координат
    def open_full_size_map(self):
        try:
            if self.dict_meta["Latitude"] and self.dict_meta["Longitude"]:
                self.map_form = MapWindow()
                self.map_form.set_cords(
                    self.dict_meta["Latitude"], self.dict_meta["Longitude"]
                )
                self.map_form.view_map(16)
                self.map_form.show()

        except Exception as e:
            print(f"Error with open map: {e}")

    # Функция для отображения мини-карты
    def view_map(self, zoom):
        if self.dict_meta["Latitude"] and self.dict_meta["Longitude"]:
            try:
                lat = float(self.dict_meta.get("Latitude"))
                lon = float(self.dict_meta.get("Longitude"))
            except (TypeError, ValueError):
                return False

            mini_map = YandexMapHandler(lat, lon)
            pixmap = mini_map.view_map(
                self.map_label.width(), self.map_label.height(), zoom
            )
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.clear()

    def open_gallery(self):
        self.gallery_form.show()

    def handle_gallery_image_selected(self, image_id: int):
        try:
            self.db.connect()

            image_blob = self.db.get_image_by_id(image_id)
            if not image_blob:
                print(f"Изображение с ID {image_id} не найдено в image_table.")
                return

            metadata = self.db.get_metadata_by_id(image_id)
            if not metadata:
                print(f"Метаданные для ID {image_id} не найдены в metadata_table.")
                return

            self.db.close()

            self.image_viewer.setImageFromBlob(image_blob)
            self.dict_meta = metadata
            self.file_path = [f"gallery_{image_id}", "Gallery Image"]

            self.filling_table()
            self.view_map(13)

            print(f"Успешно загружено изображение с ID: {image_id}")

        except Exception as e:
            print(f"Ошибка при обработке выбранного изображения: {e}")

    # Выбор файла для поиска метаданных
    def choose_file(self):
        try:
            self.file_path = QFileDialog.getOpenFileName(
                self,
                "Выбор файла",
                self.resource_path("\\var"),
                "Изображения (*.png *.jpg *.jpeg)",
            )
            if not self.file_path:
                print("Файл не выбран.")
                return
            self.image_viewer.setImageFromPath(self.file_path[0])

            if self.file_path[0].lower().endswith("jpeg"):
                self.image_viewer.rotate_clockwise_90()
            """
            После выбора файла происходит извлечение метаданных,
            добавление записей в БД, заполнение таблицы и попытка отображения карты 
            """
            self.catch_metadata()
            self.insert_to_database()
            self.filling_table()
            self.view_map(13)  # Указываем увеличение, default = 13

        except Exception as e:
            print(f"Error with choose or processing file: {e}")

    # Преобразование метаданных в словарь для последующего занесения в БД
    def catch_metadata(self):
        metadata = ImageMetadataExtractor(self.file_path[0])
        self.dict_meta = metadata.get_metadata_dict()
        print(
            "Caught metadata in dictionary (for insert into DataBase):\n\t",
            self.dict_meta,
        )

    # Непосредственное добавление в БД словаря с метаданными
    def insert_to_database(self):
        try:
            self.db.connect()
            self.db.insert_metadata(self.dict_meta)
            self.db.insert_image(self.file_path[0])
            self.db.close()

        except Exception as e:
            print(f"Error with insert to database: {e}")

    # Заполнение таблицы метаданными
    def filling_table(self):
        keys_order = [
            "NameFile",
            "Make",
            "Model",
            "Software",
            "DateTime",
            "HostComputer",
            "Mode",
            "Flash",
            "ColorSpace",
            "ExifImageWidth",
            "ExifImageHeight",
            "OffsetTime",
            "Latitude",
            "Longitude",
        ]

        if self.dict_meta is None:
            row_count = self.metadata_table.rowCount()
            for row in range(row_count):
                self.metadata_table.setItem(row, 1, QTableWidgetItem(""))
            return

        for row, key in enumerate(keys_order):
            val = (
                self.dict_meta.get(key, "")
                if self.dict_meta.get(key) is not None
                else ""
            )
            self.metadata_table.setItem(row, 1, QTableWidgetItem(str(val)))

    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
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
