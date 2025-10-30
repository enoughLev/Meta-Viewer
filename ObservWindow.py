import os
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform, QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QTableWidgetItem

from GaleryWindow import GalleryWindow
from Forms.ObservForm_ui import Ui_MainWindow

from ImageViewer import ImageViewer
from MetadataExtractor import ImageMetadataExtractor
from DatabaseWorker import MetadataDatabase

class ObserverWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("Главное окно")
        self.setWindowIcon(QIcon("C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\img\icon.png"))
        self.metadata_table.setHorizontalHeaderLabels(["", ""])
        self.metadata_table.setStyleSheet("background-color: #f0f0f0;")
        self.metadata_table.setColumnWidth(0, 170)
        self.metadata_table.setColumnWidth(1, 330)

        self.rotate_btn.setIcon(QIcon("C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\img\\rotate.png"))

        self.file_path = ""
        #self.file_path = ["C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\\var\\z.jpeg", "Static IMG"]

        self.gallery_form = GalleryWindow()

        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)
        self.img_view = ImageViewer()

        self.open_gallery_btn.clicked.connect(self.open_gallery)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.rotate_btn.clicked.connect(self.image_viewer.rotate_clockwise_90)
        self.exit_btn.clicked.connect(self.close)



    def load_data_to_tablewidget(self):
        try:
            self.conn = sqlite3.connect('Database/MetaViewerDB.db')
            self.cursor = self.conn.cursor()

            # Получаем первую запись из таблицы metadata_table
            self.cursor.execute("SELECT * FROM metadata_table LIMIT 1")
            record = self.cursor.fetchone()

            if not record:
                # Если данных нет - не меняем ключи в первом столбце, но очищаем значения во втором
                row_count = self.metadata_table.rowCount()
                for row in range(row_count):
                    self.metadata_table.setItem(row, 1, QTableWidgetItem(""))
                return

            # Получаем названия колонок (ключи), исключая 'id'
            column_names = [desc[0] for desc in self.cursor.description]
            if 'id' in column_names:
                id_index = column_names.index('id')
                # Убираем id из списков и записи
                column_names.pop(id_index)
                record = tuple(value for i, value in enumerate(record) if i != id_index)

            # Определяем порядок ключей без id, соответствующий rows в таблице на форме
            keys_order = [
                "Make", "Model", "Software", "DateTime",
                "HostComputer", "Mode", "Flash", "ColorSpace",
                "ExifImageWidth", "ExifImageHeight", "OffsetTime",
                "Latitude", "Longitude", "NameFile"
            ]

            for row, key in enumerate(keys_order):
                try:
                    idx = column_names.index(key)
                    val = record[idx] if record[idx] is not None else ""
                except ValueError:
                    val = ""
                self.metadata_table.setItem(row, 1, QTableWidgetItem(str(val)))

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")



    def open_gallery(self):
        self.gallery_form.show()

    def choose_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Выбор файла', "C:\\Users\levch\Downloads\Phone Link", 'Изображения (*.png *.jpg *.jpeg)')
        print(self.file_path)
        metadata = ImageMetadataExtractor(self.file_path[0])

        dict_meta = metadata.get_metadata_dict()
        print(dict_meta)
        db = MetadataDatabase("Database/MetaViewerDB.db")
        db.connect()
        db.insert_metadata(dict_meta)
        db.insert_image(self.file_path[0])
        record = db.fetch_metadata_by_id(1)
        self.load_data_to_tablewidget()
        #print(record)
        db.close()
        metadata.print_all_metadata()
        #self.metadata_label.setText(metadata.display_metadata())
        self.image_viewer.setImage(self.file_path[0])
        if "jpeg" in self.file_path[0]:
            self.image_viewer.rotate_clockwise_90()




