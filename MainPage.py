import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from Page import Page
from SplitHex import Hex, get_split_file_path
from Helpers import singleton


colors = {'wrong': 'red',
          'empty': 'yellow',
          'correct': 'white'}


@singleton
class MainPage(Page):

    from PyQt5.QtCore import pyqtSignal

    value_changed = pyqtSignal()

    def __init__(self, ui):
        super().__init__()

        self.ui = ui
        self.connect_signals()
        self.file_path = None
        self.ui.checkBox_ECC.setChecked(False)
        self.ui.comboBox_ECC_bits.setEnabled(False)
        self.ui.lineEdit_ECC_path.setEnabled(False)
        self.ui.label_ECC_bits.setEnabled(False)
        self.ui.label_ECC_address.setEnabled(False)

    def set_file_path(self):
        file_path = QFileDialog.getOpenFileName(None, 'Open ER_IPROM1 file',
                                                    'l:\\test_files')[0]
        if file_path:
            self.ui.lineEdit_hex_file.setText(file_path)

    def set_value(self, path):

        if self.check_path(path):
            color = colors['correct']
            self.file_path = path
        elif path is '':
            color = colors['empty']
            self.file_path = None
        else:
            color = colors['wrong']
            self.file_path = None

        self.ui.lineEdit_hex_file.setStyleSheet("border: 2px solid {};".format(color))

    def check_and_create(self):

        if os.path.isfile(self.file_path):
            bits_number = self.ui.comboBox_bits.currentText()
            banks_number = self.ui.spinBox_banks_number.value()
            if self.ui.checkBox_ECC.isChecked() and self.ui.check_ECC():
                self.ui.get_ECC(self.ui.comboBox_ECC_bits.currentText())
            hex_obj = Hex(self.file_path, bits_number, banks_number)
            hex_obj.split()
            print(self.file_path)
            self.open_page.emit('Sucsess')

    def connect_signals(self):
        self.ui.pushButton_open.clicked.connect(self.set_file_path)
        self.ui.pushButton_create.clicked.connect(self.check_and_create)
        self.ui.lineEdit_hex_file.textChanged.connect(self.set_value)
        self.ui.checkBox_ECC.stateChanged.connect(self.check_ECC)
        self.value_changed.connect(self.set_button_create)

    def check_path(self, path):

        pattern = r'.*/(ER_IROM1)$'
        from re import findall
        print(bool(findall(pattern, path)))
        return bool(findall(pattern, path))

    def set_button_create(self):
        self.ui.pushButton_create.setEnabled(bool(self.file_path))

    def check_ECC(self):
        print('Ecc')
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
        self.value_changed.emit()


    def get_ECC(self, bits):
        pass
    """
    module ECC_T(DIN, DOUT, ECC);

input  [63:0] DIN;

output [63:0] DOUT;

output [7:0] ECC;

assign DOUT=DIN;

assign ECC[0]=(^DIN[7:0])^  DIN[10]^DIN[13]^DIN[14]^DIN[17]^DIN[20]^DIN[23]^DIN[24]^DIN[27]^DIN[35]^DIN[43]^DIN[46]^DIN[47]^DIN[51]^DIN[52]^DIN[53]^DIN[56]^DIN[57]^DIN[58];

assign ECC[1]=(^DIN[15:8])^ DIN[0]^ DIN[1]^ DIN[2]^DIN[18]^DIN[21]^DIN[22]^DIN[25]^DIN[28]^DIN[31]^DIN[32]^DIN[35]^DIN[43]^DIN[51]^DIN[54]^DIN[55]^DIN[59]^DIN[60]^DIN[61];

assign ECC[2]=(^DIN[23:16])^DIN[3]^ DIN[4]^ DIN[5]^DIN[8]^DIN[9]^DIN[10]^DIN[26]^DIN[29]^DIN[30]^DIN[33]^DIN[36]^DIN[39]^DIN[40]^DIN[43]^DIN[51]^DIN[59]^DIN[62]^DIN[63];

assign ECC[3]=(^DIN[31:24])^DIN[3]^ DIN[6]^ DIN[7]^DIN[11]^DIN[12]^DIN[13]^DIN[16]^DIN[17]^DIN[18]^DIN[34]^DIN[37]^DIN[38]^DIN[41]^DIN[44]^DIN[47]^DIN[48]^DIN[51]^DIN[59];

assign ECC[4]=(^DIN[39:32])^DIN[3]^ DIN[11]^ DIN[14]^DIN[15]^DIN[19]^DIN[20]^DIN[21]^DIN[24]^DIN[25]^DIN[26]^DIN[42]^DIN[45]^DIN[46]^DIN[49]^DIN[52]^DIN[55]^DIN[56]^DIN[59];

assign ECC[5]=(^DIN[47:40])^DIN[0]^ DIN[3]^ DIN[11]^DIN[19]^DIN[22]^DIN[23]^DIN[27]^DIN[28]^DIN[29]^DIN[32]^DIN[33]^DIN[34]^DIN[50]^DIN[53]^DIN[54]^DIN[57]^DIN[60]^DIN[63];

assign ECC[6]=(^DIN[55:48])^DIN[1]^ DIN[4]^DIN[7]^DIN[8]^DIN[11]^DIN[19]^DIN[27]^DIN[30]^DIN[31]^DIN[35]^DIN[36]^DIN[37]^DIN[40]^DIN[41]^DIN[42]^DIN[58]^DIN[61]^DIN[62];

assign ECC[7]=(^DIN[63:56])^DIN[2]^ DIN[5]^DIN[6]^DIN[9]^DIN[12]^DIN[16]^DIN[15]^DIN[19]^DIN[27]^DIN[35]^DIN[38]^DIN[39]^DIN[43]^DIN[44]^DIN[45]^DIN[48]^DIN[49]^DIN[50];

endmodule

    """