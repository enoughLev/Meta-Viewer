import sys
from PyQt6.QtWidgets import QApplication
from Windows.ObserveWindow import ObserverWindow


def main():
    app = QApplication(sys.argv)
    window = ObserverWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
