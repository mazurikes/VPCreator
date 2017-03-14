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
        super().connect_signals()
        self.ui.radioButton_ecc_off.toggled.connect(self.set_state)

    def set_state(self, state):  # check using radioButton ecc_off
        DataStorage.memory_type = MemoryType.WithoutEcc if state else MemoryType.WithEcc







