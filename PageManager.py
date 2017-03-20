from PyQt5 import uic
from enum import Enum
from PyQt5.QtWidgets import *
from os import getcwd, path

from StartPage import StartPage
from SelectFilePage import SelectFilePage
from MemoryTypePage import MemoryTypePage
from WithoutEccPage import WithoutEccPage
from EccAdressPage import EccAdressPage
from BanksTypePage import BanksTypePage
from JointBanksPage import JointBanksPage
from SeparatedBanksPage import SeparatedBanksPage
from ResultPage import ResultPage

from Helpers import singleton, MemoryType
from Logger import log
from DataStorage import DataStorage

UI_PATH = path.join(getcwd(), 'ui', 'main_1203.ui')


@singleton
class PageManager(QMainWindow):
    def __init__(self):
        super().__init__()

        DataStorage()
        self.ui = self.initUi()
        self.ui.setWindowTitle('VPCreator')
        self.init_pages()
        self.pages = (
            self.Start,
            self.SelectFile,
            self.MemoryType,
            self.WithoutECC,
            self.EccAdress,
            self.BanksType,
            self.SeparatedBanks,
            self.JointBanks,
            self.Result
        )
        self.connect_signals()

        self.open_page(self.Start)
        self.__current_page = self.Start

    def initUi(self):
        return uic.loadUi(UI_PATH, self)

    def init_pages(self):
        self.Start = StartPage(self.ui)
        self.SelectFile = SelectFilePage(self.ui)
        self.MemoryType = MemoryTypePage(self.ui)
        self.WithoutECC = WithoutEccPage(self.ui)
        self.EccAdress = EccAdressPage(self.ui)
        self.BanksType = BanksTypePage(self.ui)
        self.JointBanks = JointBanksPage(self.ui)
        self.SeparatedBanks = SeparatedBanksPage(self.ui)
        self.Result = ResultPage(self.ui)

    def connect_signals(self):
        for page in self.pages:
            page.open_next.connect(self.open_next)
            page.open_previous.connect(self.open_previous)
        self.ui.pushButton_next.clicked.connect(self.open_next)
        self.ui.pushButton_previous.clicked.connect(self.open_previous)

    def open_next(self):
        self.open_page(self.get_next_after(self.current_page))

    def open_previous(self):
        self.open_page(self.get_previous_before(self.current_page))

    def open_page(self, page):
        try:
            page.prepare_to_open()
            self.ui.stackedWidget.setCurrentIndex(self.pages.index(page))
            self.current_page = page
        except Exception as e:
            log.error(e, show_caller=True)

    def get_next_after(self, page):
        if page == self.Start:
            return self.SelectFile
        elif page == self.SelectFile:
            return self.MemoryType
        elif page == self.MemoryType:
            return self.WithoutECC if DataStorage().memory_type == MemoryType.WithoutEcc else self.EccAdress
        elif page == self.WithoutECC:
            return self.Result
        elif page == self.EccAdress:
            return self.BanksType
        elif page == self.BanksType:
            return self.JointBanks if self.BanksType.type == self.BanksType.Type.Joint else self.SeparatedBanks
        elif page == self.JointBanks:
            return self.Result
        elif page == self.SeparatedBanks:
            return self.Result
        elif page == self.Result:
            return self.SelectFile
        else:
            log.error('Unknown page: {}'.format(page))
            return page

    def get_previous_before(self, page):
        if page == self.Start:
            return page
        elif page == self.SelectFile:
            return self.Start
        elif page == self.MemoryType:
            return self.SelectFile
        elif page == self.WithoutECC:
            return self.MemoryType
        elif page == self.EccAdress:
            return self.MemoryType
        elif page == self.BanksType:
            return self.EccAdress
        elif page == self.JointBanks:
            return self.BanksType
        elif page == self.SeparatedBanks:
            return self.BanksType
        elif page == self.Result:
            return page
        else:
            log.error('Unknown page: {}'.format(page))
            return page

    @property
    def current_page(self):
        return self.__current_page

    @current_page.setter
    def current_page(self, page):
        self.__current_page = page
        log.info('Current page is {}'.format(page))