from Page import Page
from ECC import ECC
from DataStorage import DataStorage
from Helpers import BanksType


class BanksTypePage(Page):

    def prepare_to_open(self):
        ECC(DataStorage().file_path).generate_ecc_and_write_to_file()
        super().prepare_to_open()
        self.ui.pushButton_next.setEnabled(True)

    def connect_signals(self):
        self.ui.pushButton_next.clicked.connect(lambda: self.open_next.emit())
        self.ui.radioButton_separated.toggled.connect(self.set_state)

    def set_state(self, state):  # check using radioButton_separated
        DataStorage().banks_type = BanksType.Separated if state else BanksType.Joint
