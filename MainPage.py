from PyQt5.QtWidgets import *
import os
from re import findall

from Page import Page
from HexSplitter import HexSplitter
from Helpers import singleton
from ECC import ECC


colors = {'wrong': 'red',
          'empty': 'yellow',
          'correct': 'white'}


@singleton
class MainPage(Page):

    def __init__(self, ui):
        super().__init__()

        self.ui = ui
        self.connect_signals()
        self.ui.checkBox_ECC.setChecked(True)
        self.ui.checkBox_ECC.setChecked(False)
        self.ui.pushButton_create.setEnabled(False)

    def set_file_path(self):
        file_path = QFileDialog.getOpenFileName(None, 'Open ER_IPROM1 file',
                                                    'l:\\Документы\\test_files')[0]
        if file_path:
            self.ui.lineEdit_hex_file.setText(file_path)

    def set_path(self, path):

        if self.check_path(path):
            color = colors['correct']
            self.file_path = path
        elif path is '':
            color = colors['empty']
            self.file_path = None
        else:
            color = colors['wrong']
            self.file_path = None

        self.ui.pushButton_create.setEnabled(bool(self.file_path))
        self.ui.lineEdit_hex_file.setStyleSheet("border: 2px solid {};".format(color))

    def check_and_create(self):

        if os.path.isfile(self.file_path):
            bits_number = self.ui.comboBox_bits.currentText()
            banks_number = self.ui.spinBox_banks_number.value()
            if self.ui.checkBox_ECC.isChecked():
                ECC(file=self.file_path)

            HexSplitter(self.file_path, bits_number, banks_number)

            print(self.file_path)
            self.open_page.emit('Sucsess')

    def connect_signals(self):
        self.ui.pushButton_open.clicked.connect(self.set_file_path)
        self.ui.pushButton_create.clicked.connect(self.check_and_create)
        self.ui.lineEdit_hex_file.textChanged.connect(self.set_path)
        self.ui.checkBox_ECC.stateChanged.connect(self.check_ECC)

    def check_path(self, path):

        pattern = r'.*/(ER_IROM1)$'
        return bool(findall(pattern, path))

    def check_ECC(self):
        flag = self.ui.checkBox_ECC.isChecked()
        self.ui.comboBox_ECC_bits.setEnabled(flag)
        self.ui.lineEdit_ECC_path.setEnabled(flag)
        self.ui.label_ECC_bits.setEnabled(flag)
        self.ui.label_ECC_address.setEnabled(flag)

    @property
    def file_path(self):
        print(str(self), ' FILE PATH ', self._file_path)
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        self._file_path = path
