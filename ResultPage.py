from Page import Page
from DataStorage import DataStorage


class ResultPage(Page):
    pass

    def __init__(self, ui):
        super().__init__(ui)

    def connect_signals(self):
        self.ui.pushButton_open_folder.clicked.connect(self.open_split_files_folder)
        self.ui.pushButton_choose_other.clicked.connect(lambda: self.open_next.emit())

    def prepare_ui(self):
        super().prepare_ui()
        self.set_label()
        self.ui.pushButton_next.setVisible(False)
        self.ui.pushButton_previous.setVisible(False)

    def set_label(self):
        if DataStorage().destination_folder:
            self.ui.label_result.setText('{} \nwas splitted.'
                                               '\nClick button to open folder with files'.
                                               format(DataStorage().file_path))

    def open_split_files_folder(self):
        path = str(DataStorage().splitted_files_directory).replace('/', '\\')
        command = 'explorer /open,"{}"'.format(path)
        from subprocess import Popen
        Popen(command)