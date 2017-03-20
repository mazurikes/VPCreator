#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
from Helpers import get_split_file_path, get_file_content, MemoryType
from DataStorage import DataStorage
from Logger import log

SIZE_OF_ONE_HEX_CHARACTER_IN_BITS = 4
NAME_OF_SPLIT_FILES_DIRECTORY = 'VPCreator'


class Splitter:
    """

    Parses input file and splits it.
    """

    def __init__(self):
        if DataStorage().memory_type == MemoryType.WithoutEcc:
            self.input_file = DataStorage().file_path
            self.file_name = DataStorage().file_name
            self.file_dir = DataStorage().file_dir
            self.splitted_files_directory = os.path.join(self.file_dir, NAME_OF_SPLIT_FILES_DIRECTORY)

            self.bits_number = DataStorage().data_bits
            self.banks_number = DataStorage().data_banks_number
            self.rar = DataStorage().data_rarefaction


        self.finished_output = []
        self.split_files_path = ''
        self.default_ext = '.vh'

        self.split()

    def split(self):
        self.create_empty_hex_files()
        self.write_split_hex_files()
        log.info('All files were written successfully')

    def get_number_of_symbols_in_input_file_string(self):
        with open(self.input_file, 'r', encoding='UTF-8') as f:
            first_string = str(f.readline().replace('\n', ''))
        return len(first_string)

    def get_number_of_symbols_in_bank_string(self):
        return int(self.bits_number / SIZE_OF_ONE_HEX_CHARACTER_IN_BITS)

    def make_result_list(self):
        file_content = get_file_content(self.input_file)
        print(len(file_content))
        result_list = []

        symbols_in_file_string = self.get_number_of_symbols_in_input_file_string()
        symbols_in_bank_string = self.get_number_of_symbols_in_bank_string()
        number_of_input_string_in_bank_string = int(symbols_in_bank_string / symbols_in_file_string)

        temp_string = ''
        counter = 0
        for index, string in enumerate(file_content):
            if counter < number_of_input_string_in_bank_string:
                temp_string = string + temp_string
                counter += 1
            else:
                result_list.append(temp_string)
                temp_string = string
                counter = 1
        print(result_list)
        self.finished_output = result_list

    def write_split_hex_files(self):
        string_number = 0
        self.make_result_list()

        list_of_files = []
        list_dir = os.listdir(self.splitted_files_directory)
        file_number = 0

        # Open empty files for the writing
        for file in list_dir:
            list_of_files.append(open(os.path.join(self.splitted_files_directory, file), 'w', encoding='UTF-8'))

        # Put input info into banks
        for index, value in enumerate(self.finished_output):
            if not index % self.banks_number:
                if not index:
                    list_of_files[0].write('@{0:<5X}{1}'.format(string_number, value) + '\n')
                    continue
                string_number += 1

            file_number = index % self.banks_number
            list_of_files[file_number].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        # Fill all banks by zero if need (all files must have the same number of string)
        if file_number != self.banks_number - 1:
            for index in range(file_number + 1, self.banks_number):
                zero_number = self.get_number_of_symbols_in_bank_string()
                value = '0' * zero_number
                list_of_files[index].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        for file in list_of_files:
            file.close()

    def create_dir(self, path):
        '''

        Creates dir 'path' if 'path' don't exists. If 'path' exists it removes all files in.
        '''

        if not os.path.exists(path):
            os.mkdir(path)
        else:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                os.remove(file_path)
        log.info('Dir {} was cleared'.format(path))

    def create_empty_hex_files(self):
        """

        Create (banks_number) empty hex files
        """
        self.create_dir(self.splitted_files_directory)
        for number in range(self.banks_number):
            full_banks_name = os.path.join(self.splitted_files_directory,
                                           self.file_name + '_{}{}'.format(number, self.default_ext))

            with open(full_banks_name, 'w'):
                log.info('File {} was created'.format(full_banks_name))
        log.info('All files was created.')

if __name__ == '__main__':
    input_file = 'L:\\Документы\\Python_projects\\Practice\\test_files\\ER_IROM1'
    obj = Splitter(input_file, 32, 4)
    # file_output = obj.get_file_output()
    # print(file_output)
    # print(len(file_output))
    obj.split()
