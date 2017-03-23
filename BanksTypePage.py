from Page import Page
from ECC import ECC
from DataStorage import DataStorage
from Helpers import BanksType


class BanksTypePage(Page):

    def prepare_to_open(self):
        ECC(DataStorage().file_path)
        super().prepare_to_open()
        self.ui.pushButton_next.setEnabled(True)

    def connect_signals(self):
        self.ui.radioButton_separated.toggled.connect(self.set_state)

    def set_state(self, state):  # check using radioButton_separated
        DataStorage().banks_type = BanksType.Separated if state else BanksType.Joint
