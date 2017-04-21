from Page import Page
from Helpers import EccLocation
from DataStorage import DataStorage
from Splitter import Splitter

DEFAULT_NUM = 1
DEFAULT_ECC = 8


class JointBanksPage(Page):

    def __init__(self, ui):
        super().__init__(ui)

    def connect_signals(self):
        self.ui.pushButton_next.setEnabled(True)

        self.ui.spinBox_num_j.valueChanged.connect(self.set_num)
        self.ui.comboBox_bits_j.currentIndexChanged.connect(self.set_bits)
        self.ui.comboBox_rar_j.currentIndexChanged.connect(self.set_rar)
        self.ui.radioButton_right.toggled.connect(self.set_state)

    def prepare_to_open(self):
        super().prepare_to_open()
        self.ui.pushButton_next.clicked.connect(lambda: self.open_next.emit())

    def set_state(self, state):  # check using radioButton_right
        DataStorage().ecc_location = EccLocation.Right if state else EccLocation.Left

    def prepare_ui(self):
        super().prepare_ui()
        self.fill()

    def fill(self):
        self.ui.spinBox_num_j.setMinimum(1)
        self.ui.spinBox_num_j.setValue(DEFAULT_NUM)
        self.set_num(DEFAULT_NUM)  # setValue doesn't emit valueChanged() because

        self.ui.comboBox_bits_j.clear()
        for i in range(3, 6):
            self.ui.comboBox_bits_j.addItem(str(2**i + DEFAULT_ECC), 2**i + DEFAULT_ECC)

        self.fill_rar()

    def fill_rar(self):
        self.ui.comboBox_rar_j.clear()
        self.ui.comboBox_rar_j.addItem(str(1), 1)
        if self.current_amount != 1:
            self.ui.comboBox_rar_j.addItem(str(self.current_amount), self.current_amount)

    def set_num(self, value):
        self.current_amount = value

    def set_bits(self, index):
        self.current_bits = index

    def set_rar(self, index):
        self.current_rar = index

    @property
    def current_amount(self):
        return self.ui.spinBox_num_j.value()

    @current_amount.setter
    def current_amount(self, value):
        if value:
            DataStorage().joint_banks_number = value
            self.fill_rar()

    @property
    def current_bits(self):
        return self.ui.comboBox_bits_j.currentData()

    @current_bits.setter
    def current_bits(self, index):
        value = self.ui.comboBox_bits_j.itemData(index)
        if value:
            DataStorage().joint_data_bits = value

    @property
    def current_rar(self):
        return self.ui.comboBox_rar_j.currentData()

    @current_rar.setter
    def current_rar(self, index):
        value = self.ui.comboBox_rar_j.itemData(index)
        if value:
            DataStorage().joint_data_rarefaction = value
