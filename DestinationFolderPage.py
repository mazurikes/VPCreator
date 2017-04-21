from PyQt5.QtWidgets import QFileDialog
from os.path import exists

from Helpers import colors
from Page import Page
from DataStorage import DataStorage
from Splitter import Splitter


class DestinationFolderPage(Page):

    def __init__(self, ui):
        super().__init__(ui)
        self._dir_path = None
        print(self)
        # self.ui.lineEdit_dir.setStyleSheet("border: 2px solid {};".format(colors['empty']))

    def connect_signals(self):
        self.ui.pushButton_open_dir.clicked.connect(self.select_dir)
        self.ui.lineEdit_dir.textChanged.connect(self.set_path)
        self.ui.pushButton_next.clicked.connect(self.create_banks)

    def prepare_to_open(self):
        super().prepare_to_open()
        self.ui.pushButton_next.setEnabled(bool(self._dir_path))
        self.ui.pushButton_next.setText('Create files')

    def select_dir(self):
        dir_path = QFileDialog.getExistingDirectory(None, caption='Choose Directory to save files')
        print('dir name={}'.format(dir_path))
        if dir_path:
            self.ui.lineEdit_dir.setText(dir_path)

    def set_path(self, path):
        if self.check_path(path):
            color = colors['correct']
            self.dir_path = path
        elif path is '':
            color = colors['empty']
            self.dir_path = None
        else:
            color = colors['wrong']
            self.dir_path = None

        self.ui.lineEdit_dir.setStyleSheet("border: 2px solid {};".format(color))

    def check_path(self, path):
        if path is None or not exists(path):
            return False
        return True

    def create_banks(self):
        try:
            Splitter()
        except Exception as e:
            print('Exception from create_banks: {}'.format(e))
        else:
            if DataStorage().file_with_ecc is not None and exists(DataStorage().file_with_ecc):
                from shutil import copyfile
                from os import remove
                copyfile(DataStorage().file_with_ecc, DataStorage().splitted_files_directory + '\\file_with_ecc.txt')
                remove(DataStorage().file_with_ecc)
        finally:
            self.open_next.emit()


    @property
    def dir_path(self):
        return self._dir_path

    @dir_path.setter
    def dir_path(self, path):
        self._dir_path = path
        DataStorage().destination_folder = self._dir_path
        self.ui.pushButton_next.setEnabled(bool(self._dir_path))
