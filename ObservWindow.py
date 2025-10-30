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

        self.setWindowTitle("Главное окно")
        self.setWindowIcon(QIcon("C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\img\icon.png"))
        #self.pushButton = QPushButton
        self.pushButton.setText("qweqwewq")
        #self.rotate_btn.setIcon(QIcon("C:\\Users\levch\Documents\ВУЗ\ЯП\\5 семестр (Python Web)\Семестровая_1\img\\rotate.png"))
        self.setupUi(self)

        #self.file_path = ""
        self.file_path = ["C:\\Users\levch\Downloads\Phone Link\\build.jpeg", "Static IMG"]

        self.open_gallery_btn.clicked.connect(self.open_gallery)
        self.choose_file_btn.clicked.connect(self.choose_file)


        self.gallery_form = GalleryWindow()

        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)
        self.img_view = ImageViewer()
        #self.image_viewer.setImage("C:\\Users\levch\Desktop\qwe.png")


    def open_gallery(self):
        self.gallery_form.show()

    def choose_file(self):
        #self.file_path = QFileDialog.getOpenFileName(self, 'Выбор файла', "C:\\Users\levch\Downloads\Phone Link", 'Изображения (*.png *.jpg *.jpeg)')
        print(self.file_path)
        metadata = ImageMetadataExtractor(self.file_path[0])
        metadata.print_all_metadata()
        self.image_viewer.setImage(self.file_path[0])
        if "jpeg" in self.file_path[0]:
            self.image_viewer.rotate_clockwise_90()




