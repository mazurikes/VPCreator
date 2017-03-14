from PyQt5.QtCore import pyqtSignal, QObject


class Page(QObject):

    open_next = pyqtSignal()
    open_previous = pyqtSignal()

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.connect_signals()

    def prepare_to_open(self):
        self.prepare_ui()

    def connect_signals(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def prepare_ui(self):
        self.ui.pushButton_next.setVisible(True)
        self.ui.pushButton_previous.setVisible(True)
        self.ui.pushButton_next.setEnabled(False)

    def fill(self):
        pass






