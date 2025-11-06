from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

'''
Пришлось создать класс с перегрузкой метода стандартного Pixmap
и добавлением пары функций, потому что иначе не хотели картинки 
вставать красиво в таблицу галереи
'''

class ScaledPixmapLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pixmap = None
        self.fixed_height = 250

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self.updatePixmap()

    def updatePixmap(self):
        if self._pixmap:
            scaled = self._pixmap.scaledToHeight(self.fixed_height, Qt.TransformationMode.SmoothTransformation)
            super().setPixmap(scaled)

    def resizeEvent(self, event):
        self.updatePixmap()
        super().resizeEvent(event)