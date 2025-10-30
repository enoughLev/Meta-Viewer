import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform, QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton

from GaleryWindow import GalleryWindow
from Forms.ObservForm_ui import Ui_MainWindow

from ImageViewer import ImageViewer
from MetadataExtractor import ImageMetadataExtractor

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

        #self.file_path = ""
        self.file_path = ["C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\\var\\z.jpeg", "Static IMG"]

        self.gallery_form = GalleryWindow()

        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)
        self.img_view = ImageViewer()

        self.open_gallery_btn.clicked.connect(self.open_gallery)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.rotate_btn.clicked.connect(self.image_viewer.rotate_clockwise_90)
        self.exit_btn.clicked.connect(self.close)



        #self.image_viewer.setImage("C:\\Users\levch\Desktop\qwe.png")


    def open_gallery(self):
        self.gallery_form.show()

    def choose_file(self):
        #self.file_path = QFileDialog.getOpenFileName(self, 'Выбор файла', "C:\\Users\levch\Downloads\Phone Link", 'Изображения (*.png *.jpg *.jpeg)')
        print(self.file_path)
        metadata = ImageMetadataExtractor(self.file_path[0])

        metadata.print_all_metadata()
        self.metadata_label.setText(metadata.display_metadata())
        self.image_viewer.setImage(self.file_path[0])
        if "jpeg" in self.file_path[0]:
            self.image_viewer.rotate_clockwise_90()




