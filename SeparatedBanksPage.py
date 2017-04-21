from Page import Page
from DataStorage import DataStorage
from Splitter import Splitter

DEFAULT_NUM = 1


class SeparatedBanksPage(Page):
    def __init__(self, ui):
        super().__init__(ui)

    def connect_signals(self):
        self.ui.pushButton_next.setEnabled(True)
        self.ui.pushButton_next.clicked.connect(lambda: self.open_next.emit())

        self.ui.spinBox_data_num.valueChanged.connect(self.set_data_num)
        self.ui.comboBox_data_bits.currentIndexChanged.connect(self.set_data_bits)
        self.ui.comboBox_data_rar.currentIndexChanged.connect(self.set_data_rar)

        self.ui.spinBox_ecc_num.valueChanged.connect(self.set_ecc_num)
        self.ui.comboBox_ecc_bits.currentIndexChanged.connect(self.set_ecc_bits)
        self.ui.comboBox_ecc_rar.currentIndexChanged.connect(self.set_ecc_rar)

    def prepare_ui(self):
        super().prepare_ui()
        self.fill_data_banks()
        self.fill_ecc_banks()

    def fill_data_banks(self):
        self.ui.spinBox_data_num.setMinimum(1)
        self.ui.spinBox_data_num.setValue(DEFAULT_NUM)

        self.ui.comboBox_data_bits.clear()
        for i in range(3, 6):
            self.ui.comboBox_data_bits.addItem(str(2**i), 2**i)

        self.fill_data_rar()

    def fill_ecc_banks(self):
        self.ui.spinBox_ecc_num.setMinimum(1)
        self.ui.spinBox_ecc_num.setValue(DEFAULT_NUM)

        self.ui.comboBox_ecc_bits.clear()
        for i in range(3, 6):
            self.ui.comboBox_ecc_bits.addItem(str(2**i), 2**i)

        self.fill_ecc_rar()

    def fill_data_rar(self):
        self.ui.comboBox_data_rar.clear()
        self.ui.comboBox_data_rar.addItem(str(1), 1)
        if self.data_current_amount != 1:
            self.ui.comboBox_data_rar.addItem(str(self.data_current_amount), self.data_current_amount)

    def fill_ecc_rar(self):
        self.ui.comboBox_ecc_rar.clear()
        self.ui.comboBox_ecc_rar.addItem(str(1), 1)
        if self.ecc_current_amount != 1:
            self.ui.comboBox_ecc_rar.addItem(str(self.ecc_current_amount), self.ecc_current_amount)

    def set_data_num(self, value):
        self.data_current_amount = value

    def set_data_bits(self, index):
        self.data_current_bits = index

    def set_data_rar(self, index):
        self.data_current_rar = index

    @property
    def data_current_amount(self):
        return self.ui.spinBox_data_num.value()

    @data_current_amount.setter
    def data_current_amount(self, value):
        if value:
            DataStorage().data_banks_number = value
            self.fill_data_rar()

    @property
    def data_current_bits(self):
        return self.ui.comboBox_data_bits.currentData()

    @data_current_bits.setter
    def data_current_bits(self, index):
        value = self.ui.comboBox_data_bits.itemData(index)
        if value:
            DataStorage().data_bits = value

    @property
    def data_current_rar(self):
        return self.ui.comboBox_data_rar.currentData()

    @data_current_rar.setter
    def data_current_rar(self, index):
        value = self.ui.comboBox_data_rar.itemData(index)
        if value:
            DataStorage().data_rarefaction = value

    def set_ecc_num(self, value):
        self.ecc_current_amount = value

    def set_ecc_bits(self, index):
        self.ecc_current_bits = index

    def set_ecc_rar(self, index):
        self.ecc_current_rar = index

    @property
    def ecc_current_amount(self):
        return self.ui.spinBox_ecc_num.value()

    @ecc_current_amount.setter
    def ecc_current_amount(self, value):
        if value:
            DataStorage().ecc_banks_number = value
            self.fill_ecc_rar()

    @property
    def ecc_current_bits(self):
        return self.ui.comboBox_ecc_bits.currentData()

    @ecc_current_bits.setter
    def ecc_current_bits(self, index):
        value = self.ui.comboBox_ecc_bits.itemData(index)
        if value:
            DataStorage().ecc_bits = value

    @property
    def ecc_current_rar(self):
        return self.ui.comboBox_ecc_rar.currentData()

    @ecc_current_rar.setter
    def ecc_current_rar(self, index):
        value = self.ui.comboBox_ecc_rar.itemData(index)
        if value:
            DataStorage().ecc_rarefaction = value
