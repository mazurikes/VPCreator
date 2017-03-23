from Page import Page
from ECC import ECC
from DataStorage import DataStorage


class BanksTypePage(Page):

    def prepare_to_open(self):
        ECC(DataStorage().file_path)
        super().prepare_to_open()
