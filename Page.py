from PyQt5.QtCore import pyqtSignal, QObject


class Page(QObject):

    open_next = pyqtSignal()
    open_previous = pyqtSignal()

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def prepare_to_open(self):
        raise NotImplementedError('prepare_to_open() not implement in {}'.format(self))

    def __repr__(self):
        return self.__name__




