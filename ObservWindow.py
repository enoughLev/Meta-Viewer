from PyQt6.QtWidgets import QMainWindow, QFileDialog

from GaleryWindow import GalleryWindow
from Forms.ObservForm_ui import Ui_MainWindow
from ImageViewer import ImageViewer


class ObserverWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно")
        self.setupUi(self)

        self.file_path = ""

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
        self.file_path = QFileDialog.getOpenFileName(self, 'Выбор файла', "C:\\Users\levch\Desktop", 'Изображения (*.png *.jpg)')
        print(self.file_path)
        self.image_viewer.setImage(self.file_path[0])




