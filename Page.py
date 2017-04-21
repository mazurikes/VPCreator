from PyQt5.QtCore import pyqtSignal, QObject


class Page(QObject):

    open_next = pyqtSignal()
    open_previous = pyqtSignal()

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def prepare_to_open(self):
        self.prepare_ui()
        try:
            self.ui.pushButton_next.disconnect()
        except:
            pass
        self.connect_signals()

    def connect_signals(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def prepare_ui(self):
        self.ui.pushButton_next.setVisible(True)
        self.ui.pushButton_previous.setVisible(True)

    def fill(self):
        pass






