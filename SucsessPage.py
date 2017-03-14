from Page import Page
from SplitHex import get_split_file_path


class SucsessPage(Page):

    def __init__(self, ui):
        super().__init__()

        self.ui = ui
        self.connect_signals()

    def connect_signals(self):
        self.ui.pushButton_open_folder.clicked.connect(self.open_split_files_folder)
        self.ui.pushButton_choose_other.clicked.connect(self.open_main)

    def late_init(self, split_files_path):

        self.split_files_path = split_files_path
        self.path_dict = get_split_file_path(self.split_files_path)

        self.set_label()

    def set_label(self):
        if self.path_dict:
            self.ui.label_process_info.setText('{} was splitted.'
                                           '\nClick button to open folder with files'.format(self.path_dict['file_name']))

    def open_split_files_folder(self):
        path = str(self.path_dict['directory']).replace('/', '\\')
        command = 'explorer /open,"{}"'.format(path)
        print(command)
        from subprocess import Popen
        Popen(command)

    def open_main(self):
        self.reset_info()
        self.open_page.emit('Main')

    def reset_info(self):
        self.reset.emit()