# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from MainWindow.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
