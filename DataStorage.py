import os
from Helpers import Singleton, get_split_file_path, MemoryType, BanksType, EccLocation
from Logger import log


class DataStorage(metaclass=Singleton):
    def __init__(self):
        self.programm_location = os.path.dirname(os.path.realpath(__file__))
        self.__file_path = None
        self.destination_folder = None
        self.file_dir = None
        self.file_name = None
        self.file_extension = None
        self.splitted_files_directory = None

        # Without ecc or separated banks
        self.data_banks_number = 1
        self.data_bits = 8
        self.data_rarefaction = 1

        # if BanksType Separated
        self.ecc_banks_number = 1
        self.ecc_bits = 8
        self.ecc_rarefaction = 1

        self.memory_type = MemoryType.WithoutEcc

        # With ecc
        self.start_ecc_address = None
        self.file_with_ecc = None
        self.banks_type = BanksType.Joint

        # if BanksType Joint
        self.joint_banks_number = 1
        self.joint_data_bits = 8
        self.joint_data_rarefaction = 1
        self.ecc_location = EccLocation.Right
        # joint = (self.joint_banks_number,
        #          self.joint_data_bits - self.ecc_bits,
        #          self.joint_data_rarefaction,
        #          self.ecc_location
        #          )

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

