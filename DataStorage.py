from Helpers import singleton, get_split_file_path
from Logger import log

@singleton
class DataStorage:
    def __init__(self):
        self.__file_path = None
        self.file_dir = None
        self.file_name = None
        self.file_extension = None

        self.memory_type = None

        self.start_ecc_address = None
        self.banks_type = None

        self.optional = (
            self.start_ecc_address,
            self.banks_type
        )

    def reset(self):
        for var in self.__dict__:
            self.__setattr__(var, None)

    def __setattr__(self, key, value):
        log.info('DataStorage\'s "{}" changed to "{}"'.format(key, value))
        super().__setattr__(key, value)

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, path):
        self.__file_path = path
        split_path = get_split_file_path(self.__file_path)
        self.file_dir = split_path['directory']
        self.file_name = split_path['file_name']
        self.file_extension = split_path['extention']
