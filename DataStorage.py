from Helpers import Singleton, get_split_file_path, MemoryType, BanksType
from Logger import log


class DataStorage(metaclass=Singleton):
    def __init__(self):
        self.__file_path = None
        self.file_dir = None
        self.file_name = None
        self.file_extension = None

        # Without ecc
        self.data_banks_number = None
        self.data_bits = None
        self.data_rarefaction = None

        self.memory_type = MemoryType.WithoutEcc

        # With ecc
        self.start_ecc_address = None
        self.file_with_ecc = None
        self.banks_type = BanksType.Joint

    def reset(self):
        for var in self.__dict__:
            self.__setattr__(var, None)

    def __setattr__(self, key, value):
        log.info('DataStorage\'s "{}" changed to {} {}'.format(key, type(value), value))
        super().__setattr__(key, value)

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, path):
        self.__file_path = path
        if self.__file_path:
            split_path = get_split_file_path(self.__file_path)
            self.file_dir = split_path['directory']
            self.file_name = split_path['file_name']
            self.file_extension = split_path['extention']
        else:
            self.file_dir = None
            self.file_name = None
            self.file_extension = None

