import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QTransform
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QHBoxLayout
from Forms.GalleryForm_ui import Ui_Form
from Workers.DatabaseWorker import MetadataDatabase
from Workers.PixmapWorker import ScaledPixmapLabel


class GalleryWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.data_base = None
        self.meta_for_gallery = None
        self.setupUi(self)
        self.setWindowTitle("MetaViewer")
        self.setWindowIcon(QIcon(self.resource_path("\img\\icon.png")))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(800, 575)

        self.galery_table.setColumnWidth(0, 500)
        self.galery_table.setColumnWidth(1, 140)
        self.galery_table.setColumnWidth(2, 140)


    # Отображение таблицы при первичном открытии формы
    def show(self):
        self.data_base = MetadataDatabase(self.resource_path("\Database\MetaViewerDB.db"))
        self.get_meta_from_base()
        self.fill_table()
        super().show()


    # Получаем данные из БД в виде словаря
    def get_meta_from_base(self):
        try:
            self.data_base.connect()
            self.meta_for_gallery = self.data_base.fetch_images_and_names()
            self.data_base.close()
        except Exception as e:
            print(f"Error wih getting meta from database: {e}")


    # Прописаны все необходимые действия для заполнения таблицы
    def fill_table(self):
        try:
            fixed_height = 250
            data = self.meta_for_gallery  # словарь {id: [name, photo]}

            if self.galery_table.rowCount() < len(data):
                self.galery_table.setRowCount(len(data))

            self.galery_table.verticalHeader().setDefaultSectionSize(fixed_height)

            for i, (id_, (name, photo)) in enumerate(data.items()):
                pixmap = QPixmap()
                if not pixmap.loadFromData(photo):
                    print(f"Unable to load image {name} with ID {id_}")
                    continue

                if "jpeg" in name.lower():
                    pixmap = pixmap.transformed(QTransform().rotate(90))

                # Label с переписанным Pixmap
                label = ScaledPixmapLabel()
                label.setPixmap(pixmap)
                label.fixed_height = fixed_height
                label.updatePixmap()

                # Создание контейнеров для нормального размещения фото
                container_img = QWidget()
                layout_img = QHBoxLayout(container_img)
                layout_img.setContentsMargins(0, 0, 0, 0)
                layout_img.addWidget(label)
                layout_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_img.setLayout(layout_img)
                container_img.setFixedHeight(fixed_height)

                self.galery_table.setCellWidget(i, 0, container_img)
                self.galery_table.setRowHeight(i, fixed_height)

                item_name = QTableWidgetItem(str(name))
                item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.galery_table.setItem(i, 1, item_name)

                btn_open = QPushButton("Открыть")
                btn_delete = QPushButton("Удалить")

                # События на кнопки
                btn_delete.clicked.connect(lambda checked, row_id=id_: self.delete_row_from_base(row_id))

                # Контейнер для кнопок
                container_btn = QWidget()
                btn_layout = QHBoxLayout(container_btn)
                btn_layout.setContentsMargins(0, 0, 0, 0)
                btn_layout.addWidget(btn_open)
                btn_layout.addWidget(btn_delete)
                btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                container_btn.setLayout(btn_layout)

                self.galery_table.setCellWidget(i, 2, container_btn)

        except Exception as e:
            print(f"Error with filling table: {e}")


    # Вызывает методы удаления строки из БД
    # и перезаписи таблицы
    def delete_row_from_base(self, row):
        try:
            self.data_base.connect()
            self.data_base.delete_row(row)
            self.get_meta_from_base()
            self.galery_table.setRowCount(0)
            self.fill_table()
            self.data_base.close()
        except Exception as e:
            print(f"Error: {e}")


    def open_main_window(self):
        self.close()


    # Нужно для корректного обращения к файлам в проекте даже в EXE
    @staticmethod
    def resource_path(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        path = base_path + relative_path
        return path
