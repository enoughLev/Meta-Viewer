from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from Forms.GalleryForm_ui import Ui_Form

class GalleryWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.to_main_btn.clicked.connect(self.open_main_window)

    def open_main_window(self):
        self.close()


