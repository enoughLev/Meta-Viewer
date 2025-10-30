from PyQt6.QtWidgets import QMainWindow

from GaleryWindow import GalleryWindow
from Forms.ObservForm_ui import Ui_MainWindow
from ImageViewer import ImageViewer


class ObserverWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно")
        self.setupUi(self)

        self.open_gallery_btn.clicked.connect(self.open_gallery)

        self.gallery_form = GalleryWindow()

        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)
        self.img_view = ImageViewer()
        self.image_viewer.setImage("C:\\Users\levch\Desktop\qwe.png")


    def open_gallery(self):
        self.gallery_form.show()




