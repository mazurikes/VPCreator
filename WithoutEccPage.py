from Page import Page
from DataStorage import DataStorage
from Splitter import Splitter

DEFAULT_NUM = 1  # Default value of number of data banks


class WithoutEccPage(Page):
    def __init__(self, ui):
        super().__init__(ui)

    def connect_signals(self):
        self.ui.pushButton_next.setEnabled(True)
        self.ui.pushButton_next.clicked.connect(lambda: self.open_next.emit())

        self.ui.spinBox_num.valueChanged.connect(self.set_num)
        self.ui.comboBox_bits.currentIndexChanged.connect(self.set_bits)
        self.ui.comboBox_rar.currentIndexChanged.connect(self.set_rar)

    def prepare_ui(self):
        super().prepare_ui()
        self.fill()

    def fill(self):
        self.ui.spinBox_num.setMinimum(1)
        self.ui.spinBox_num.setValue(DEFAULT_NUM)

        self.ui.comboBox_bits.clear()
        for i in range(3, 6):
            self.ui.comboBox_bits.addItem(str(2**i), 2**i)

        self.fill_rar()

    def fill_rar(self):
        self.ui.comboBox_rar.clear()
        self.ui.comboBox_rar.addItem(str(1), 1)
        if self.current_amount != 1:
            self.ui.comboBox_rar.addItem(str(self.current_amount), self.current_amount)

    def set_num(self, value):
        self.current_amount = value

    def set_bits(self, index):
        self.current_bits = index

    def set_rar(self, index):
        self. current_rar = index

    @property
    def current_amount(self):
        return self.ui.spinBox_num.value()

    @current_amount.setter
    def current_amount(self, value):
        if value:
            DataStorage().data_banks_number = value
            self.fill_rar()

    @property
    def current_bits(self):
        return self.ui.comboBox_bits.currentData()

    @current_bits.setter
    def current_bits(self, index):
        value = self.ui.comboBox_bits.itemData(index)
        if value:
            DataStorage().data_bits = value

    @property
    def current_rar(self):
        return self.ui.comboBox_rar.currentData()

    @current_rar.setter
    def current_rar(self, index):
        value = self.ui.comboBox_rar.itemData(index)
        if value:
            DataStorage().data_rarefaction = value







