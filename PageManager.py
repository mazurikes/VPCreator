from PyQt5 import uic
from enum import Enum
from PyQt5.QtWidgets import *

from Exeptions import WrongPageName
from StartPage import StartPage
from MainPage import MainPage
from SucsessPage import SucsessPage
from Helpers import singleton


class Page(Enum):
    page_1 = 1
    page_2 = 2
    page_3 = 3


@singleton
class PageManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.all_ui.setWindowTitle('Hex Splitter')
        self.init_pages()
        self.connect_signals()

        self.open_page('Start')

    def initUi(self):
        self.all_ui = uic.loadUi('ui//new_main.ui', self)

    def init_pages(self):
        self.Start = StartPage(self.all_ui)
        self.Main = MainPage(self.all_ui)
        self.Sucsess = SucsessPage(self.all_ui)

    def connect_signals(self):
        self.Start.open_next.connect(self.set_next)
        self.Main.open_page.connect(self.open_page)
        self.Sucsess.open_page.connect(self.open_page)
        self.Sucsess.reset.connect(self.reset)

    def get_ui(self, class_object):
        self.page_name = class_object.__class__.__name__

        if self.page_name:
            if self.page_name == 'StartWindow':
                return self.all_ui.page_1
            elif self.page_name == 'MainWindow':
                return self.all_ui.page_2
            elif self.page_name == 'SucsessWindow':
                return self.all_ui.page_3
        raise WrongPageName('Wrong page: {}'.format(self.page_name))

    def open_page(self, page):

        # self.reset_info()

        if page == 'Start':
            self.all_ui.stackedWidget.setCurrentIndex(0)
        elif page == 'Main':
            self.all_ui.stackedWidget.setCurrentIndex(1)
        elif page == 'Sucsess':
            self.all_ui.stackedWidget.setCurrentIndex(2)
            self.Sucsess.late_init(self.Main.file_path)
        else:
            raise NameError('Wrong page name: \"{}\"'.format(page))

    def reset(self):
        # add reset of other lines
        self.all_ui.lineEdit_hex_file.setText('')

    def set_next(self):
        last_index = self.all_ui.stackedWidget.currentIndex()
        if last_index < self.all_ui.stackedWidget.count():
            self.all_ui.stackedWidget.setCurrentIndex(last_index + 1)

    def set_previous(self):
        last_index = self.all_ui.stackedWidget.currentIndex()
        if last_index:
            self.all_ui.stackedWidget.setCurrentIndex(last_index - 1)