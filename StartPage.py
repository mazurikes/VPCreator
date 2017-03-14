from Helpers import singleton
from Page import Page


@singleton
class StartPage(Page):

    def __init__(self, ui):
        super().__init__(ui)

    def connect_signals(self):
        self.ui.pushButton_start.clicked.connect(lambda: self.open_next.emit())

    def prepare_ui(self):
        self.ui.pushButton_next.setVisible(False)
        self.ui.pushButton_previous.setVisible(False)

