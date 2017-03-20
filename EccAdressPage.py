from Page import Page
from Helpers import get_number_of_global_adress_symbols
from DataStorage import DataStorage


class EccAdressPage(Page):
    def __init__(self, ui):
        super().__init__(ui)

    def prepare_ui(self):
        self.ui.lineEdit_ecc_adress.setInputMask('h' * self.adress_len)
        self.ui.pushButton_next.setEnabled(bool(self._adress))

    def connect_signals(self):
        super().connect_signals()
        self.ui.lineEdit_ecc_adress.textChanged.connect(self.set_adress)

    def prepare_to_open(self):
        self._adress = DataStorage().start_ecc_address
        self.adress_len = get_number_of_global_adress_symbols(DataStorage().file_path)
        super().prepare_to_open()

    def set_adress(self, adress):
        if len(adress) == self.adress_len:
            DataStorage().start_ecc_address = adress.upper()
        else:
            DataStorage().start_ecc_address = None
        self.ui.pushButton_next.setEnabled(bool(DataStorage().start_ecc_address))



