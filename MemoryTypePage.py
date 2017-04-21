from Page import Page
from DataStorage import DataStorage
from Helpers import MemoryType


class MemoryTypePage(Page):
    def __init__(self, ui):
        super().__init__(ui)

    def prepare_to_open(self):
        super().prepare_to_open()
        self.ui.pushButton_next.setEnabled(True)

    def connect_signals(self):
        self.ui.radioButton_ecc_off.toggled.connect(self.set_state)
        self.ui.pushButton_next.clicked.connect(self.open_next_new)

    def set_state(self, state):  # check using radioButton ecc_off
        DataStorage().memory_type = MemoryType.WithoutEcc if state else MemoryType.WithEcc

    def open_next_new(self):
        self.open_next.emit()







