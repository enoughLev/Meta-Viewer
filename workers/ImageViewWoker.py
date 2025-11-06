from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor, QMouseEvent, QWheelEvent, QTransform

'''
Огромный и сложный класс для красивого размещения фото в главном окне...
'''


class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(591, 781)
        self.setStyleSheet("background-color: #333333;")

        self._center_offset_computed = None
        self.pixmap_original = None
        self.scale_factor = 1.0
        self.dragging = False
        self.current_angle = 0

        self.drag_start_pos = QPoint()  # Объект для центровки фото
        self.offset = QPoint(0, 0)


    # Функция для поворота изображения
    def rotate_clockwise_90(self):
        if not self.pixmap_original:
            return
        self.current_angle = (self.current_angle + 90) % 180

        transform = (QTransform())
        transform.rotate(90)
        transform.translate(0, -self.pixmap_original.width())
        self.pixmap_original = self.pixmap_original.transformed(transform)
        label_size = self.size()
        scale_w = label_size.width() / self.pixmap_original.width()
        scale_h = label_size.height() / self.pixmap_original.height()
        self.scale_factor = min(scale_w, scale_h, 1.0)

        self.updatePixmap()


    # Установка изображения в область
    def setImage(self, image_path):
        pix = QPixmap(image_path)
        if pix.isNull():
            print("Error with load image")
            return
        self.pixmap_original = pix

        label_size = self.size()
        scale_w = label_size.width() / pix.width()
        scale_h = label_size.height() / pix.height()
        self.scale_factor = min(scale_w, scale_h, 1.0)  # не увеличиваем больше 100%

        scaled_pix = pix.scaled(
            int(pix.width() * self.scale_factor),
            int(pix.height() * self.scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем изображение
        self.setPixmap(scaled_pix)


    # Обновляет состояние изображения после перетаскивания/увеличения масштаба
    def updatePixmap(self):
        if not self.pixmap_original:
            return

        size = self.pixmap_original.size() * self.scale_factor
        scaled_pix = self.pixmap_original.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        final_pix = QPixmap(self.size())
        final_pix.fill(QColor("#333333"))

        if not hasattr(self, '_center_offset_computed'):
            self.offset = QPoint(
                (self.width() - scaled_pix.width()) // 2,
                (self.height() - scaled_pix.height()) // 2
            )
            self._center_offset_computed = True

        painter = QPainter(final_pix)
        painter.drawPixmap(self.offset, scaled_pix)
        painter.end()

        self.setPixmap(final_pix)


    # Перегрузка прокручивания колеса мыши
    def wheelEvent(self, event: QWheelEvent):
        if self.pixmap_original is None:
            return

        old_scale = self.scale_factor
        angle_delta = event.angleDelta().y()
        if angle_delta > 0:
            self.scale_factor *= 1.1
        else:
            self.scale_factor /= 1.1

        self.scale_factor = max(0.1, min(self.scale_factor, 5))

        pos = event.position().toPoint()

        delta_x = pos.x() - self.offset.x()
        delta_y = pos.y() - self.offset.y()

        new_offset_x = pos.x() - (delta_x * (self.scale_factor / old_scale))
        new_offset_y = pos.y() - (delta_y * (self.scale_factor / old_scale))

        self.offset = QPoint(int(new_offset_x), int(new_offset_y))

        self.updatePixmap()


    # Перегрузка для перетаскивания изображения
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.pos()


    # Перегрузка для перетаскивания изображения
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            delta = event.pos() - self.drag_start_pos
            self.offset += delta
            self.drag_start_pos = event.pos()
            self.updatePixmap()


    # Перегрузка для перетаскивания изображения
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
