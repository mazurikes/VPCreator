from PyQt5.QtWidgets import QFileDialog
from re import findall

from Helpers import singleton, colors
from Page import Page
from DataStorage import DataStorage


DEFAULT_DIR = 'l:\\Документы\\test_files'


@singleton
class SelectFilePage(Page):

    def __init__(self, ui):
        super().__init__(ui)
        self.__file_path = None
        self.ui.lineEdit_file.setStyleSheet("border: 2px solid {};".format(colors['empty']))

    def connect_signals(self):
        self.ui.pushButton_open.clicked.connect(self.select_file)
        self.ui.lineEdit_file.textChanged.connect(self.set_path)

    def select_file(self):
        file_path = QFileDialog.getOpenFileName(None, 'Open ER_IPROM1 file', DEFAULT_DIR)[0]
        if file_path:
            self.ui.lineEdit_file.setText(file_path)

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

        self.ui.lineEdit_file.setStyleSheet("border: 2px solid {};".format(color))

    def check_path(self, path):
        pattern = r'.*/(ER_IROM1)$'
        return bool(findall(pattern, path))

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, path):
        self.__file_path = path
        DataStorage().file_path = self.__file_path
        self.ui.pushButton_next.setEnabled(bool(self.__file_path))
