from Helpers import singleton
from Page import Page


@singleton
class StartPage(Page):

    def __init__(self, ui):
        super().__init__()

        self.ui = ui
        self.connect_signals()

    def connect_signals(self):
        self.ui.pushButton_start.clicked.connect(self.open_page_main)

    def open_page_main(self):
        self.open_next.emit()
