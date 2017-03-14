from PyQt5.QtCore import pyqtSignal, QObject


class Page(QObject):

    open_next = pyqtSignal()
    open_previous = pyqtSignal()
    open_page = pyqtSignal(str)
    reset = pyqtSignal()
