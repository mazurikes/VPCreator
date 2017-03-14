import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory

from PageManager import PageManager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = PageManager()
    # window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())