#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
from Helpers import get_ecc, get_file_content, MemoryType, BanksType, EccLocation
from DataStorage import DataStorage
from Logger import log

SIZE_OF_ONE_HEX_CHARACTER_IN_BITS = 4
NAME_OF_SPLIT_FILES_DIRECTORY = 'VPCreator'
ECC_BITS = 8


class Splitter:
    """

    Parses input file and splits it.
    """

    def __init__(self):
        self.input_file = DataStorage().file_path
        self.file_name = DataStorage().file_name
        self.file_dir = DataStorage().destination_folder
        self.splitted_files_directory = os.path.join(self.file_dir, NAME_OF_SPLIT_FILES_DIRECTORY)
        DataStorage().splitted_files_directory = self.splitted_files_directory
        self.is_ecc = not (DataStorage().memory_type == MemoryType.WithoutEcc)

        if DataStorage().memory_type == MemoryType.WithoutEcc:
            self.bits_number = DataStorage().data_bits
            self.banks_number = DataStorage().data_banks_number
            self.rar = DataStorage().data_rarefaction
        elif DataStorage().banks_type == BanksType.Joint:
            self.joint_bits_number = DataStorage().joint_data_bits
            self.bits_number = self.joint_bits_number - ECC_BITS
            self.banks_number = DataStorage().joint_banks_number
            self.rar = DataStorage().joint_data_rarefaction
            self.ecc_location = DataStorage().ecc_location
        elif DataStorage().banks_type == BanksType.Separated:
            self.bits_number = DataStorage().data_bits
            self.banks_number = DataStorage().data_banks_number
            self.rar = DataStorage().data_rarefaction
            self.ecc_bits_number = DataStorage().ecc_bits
            self.ecc_banks_number = DataStorage().ecc_banks_number
            self.ecc_rar = DataStorage().ecc_rarefaction
        else:
            raise NameError('Incorrect Memory type or Banks type')

        self.finished_output = []
        self.split_files_path = ''
        self.default_ext = '.vh'

        self.split()

    def split(self):
        if DataStorage().memory_type == MemoryType.WithoutEcc or DataStorage().banks_type != BanksType.Separated:
            self.create_empty_hex_files(data_banks=self.banks_number)
        else:
            self.create_empty_hex_files(data_banks=self.banks_number, ecc_banks=self.ecc_banks_number)

        self.write_split_hex_files(self.banks_number)
        if DataStorage().memory_type != MemoryType.WithoutEcc and DataStorage().banks_type == BanksType.Separated:
            self.write_ecc_files()
        log.info('All files were written successfully')

    def get_number_of_symbols_in_input_file_string(self):
        with open(self.input_file, 'r', encoding='UTF-8') as f:
            first_string = str(f.readline().replace('\n', ''))
        return len(first_string)

    def get_number_of_symbols_in_bank_string(self, bits_number):
        return int(bits_number / SIZE_OF_ONE_HEX_CHARACTER_IN_BITS)

    def make_result_list(self):
        file_content = get_file_content(self.input_file)
        ecc = None
        is_ecc_need = DataStorage().memory_type == MemoryType.WithEcc


        if is_ecc_need and DataStorage().banks_type == BanksType.Joint:
            ecc = get_ecc(DataStorage().file_with_ecc)

        result_list = []

        symbols_in_file_string = self.get_number_of_symbols_in_input_file_string()
        symbols_in_bank_string = self.get_number_of_symbols_in_bank_string(self.bits_number)
        number_of_input_string_in_bank_string = int(symbols_in_bank_string / symbols_in_file_string)

        temp_string = ''
        ecc_string = ''
        counter = 0

        for index, string in enumerate(file_content):
            # add ecc to string
            if is_ecc_need and DataStorage().banks_type == BanksType.Joint and ((index + 1) % 4 == 0):

                ecc_index = int(((index + 1) / 4)) - 1
                try:
                    ecc_string = '*' + ecc[ecc_index] + '*'
                except:
                    ecc_string = '*' + '00' + '*'

            if counter < number_of_input_string_in_bank_string:
                temp_string = string + temp_string
                counter += 1
            else:
                if is_ecc_need and DataStorage().banks_type == BanksType.Joint and index % 4 == 0:
                    if self.ecc_location == EccLocation.Right:
                        temp_string = temp_string + ecc_string
                    else:
                        temp_string = ecc_string + temp_string
                result_list.append(temp_string)
                temp_string = string
                counter = 1

        self.finished_output = result_list

    def make_aditional_null_list(self, result_list_lenght):
        one_file_lenght = DataStorage().file_lenght
        banks_number = DataStorage().joint_banks_number if DataStorage().banks_type == BanksType.Joint \
            else DataStorage().data_banks_number
        symbols_in_bank_string = self.get_number_of_symbols_in_bank_string(self.bits_number)
        symbols_in_input_file_string = self.get_number_of_symbols_in_input_file_string()


        # Добавляем инфу, если объем выходных файлов больше полученных данных
        total_string_number = banks_number * one_file_lenght
        zero_list = []
        if result_list_lenght < total_string_number:
            number_of_needed_null_string = total_string_number - result_list_lenght
            temp_file = DataStorage().file_dir + 'temp.txt'
            zero_list = [symbols_in_bank_string * '0' for _ in range(0, number_of_needed_null_string + 1)]

            with open(temp_file, 'w') as f:
                total_zero_number = len(zero_list) * symbols_in_bank_string
                for _ in range(0, total_zero_number // 2 + 1):
                    f.write('00\n')

            from ECC import ECC
            ECC(temp_file).prepare_and_calc_ECC()




    def write_ecc_files(self):
        string_number = 0
        ecc_bits = DataStorage().ecc_bits
        banks_number = DataStorage().ecc_banks_number
        ecc_list = get_ecc(DataStorage().file_with_ecc)

        # change ecc if ecc_bits is more that 8 bit (2 symbols)
        symbols_in_string = int(len(ecc_list[0]))
        if symbols_in_string * SIZE_OF_ONE_HEX_CHARACTER_IN_BITS != ecc_bits:
            zero_number = ecc_bits // SIZE_OF_ONE_HEX_CHARACTER_IN_BITS - symbols_in_string
            finished_output = ['0' * zero_number + ecc_item for ecc_item in ecc_list]
        else:
            finished_output = ecc_list

        list_of_files = []
        list_dir = os.listdir(self.splitted_files_directory)
        file_number = 0

        # Open empty files for the writing
        for file in list_dir:
            if 'ECC' in file:
                list_of_files.append(open(os.path.join(self.splitted_files_directory, file), 'w', encoding='UTF-8'))

        # Put ecc info into banks
        for index, value in enumerate(finished_output):
            if not index % banks_number:
                if not index:
                    list_of_files[0].write('@{0:<5X}{1}'.format(string_number, value) + '\n')
                    continue
                string_number += 1

            file_number = index % banks_number
            list_of_files[file_number].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        # Fill all banks by zero if need (all files must have the same number of string)
        if file_number != banks_number - 1:
            for index in range(file_number + 1, banks_number):
                zero_number = self.get_number_of_symbols_in_bank_string(bits_number=ecc_bits)
                value = '0' * zero_number
                list_of_files[index].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        for file in list_of_files:
            file.close()

    def write_split_hex_files(self, banks_number):
        string_number = 0
        self.make_result_list()

        list_of_files = []
        list_dir = os.listdir(self.splitted_files_directory)
        file_number = 0

        # Open empty files for the writing
        for file in list_dir:
            if 'ECC' not in file:
                list_of_files.append(open(os.path.join(self.splitted_files_directory, file), 'w', encoding='UTF-8'))

        # Put input info into banks
        for index, value in enumerate(self.finished_output):
            if not index % banks_number:
                if not index:
                    list_of_files[0].write('@{0:<5X}{1}'.format(string_number, value) + '\n')
                    continue
                string_number += 1

            file_number = index % banks_number
            list_of_files[file_number].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        # Fill all banks by zero if need (all files must have the same number of string)
        if file_number != banks_number - 1:
            for index in range(file_number + 1, banks_number):
                zero_number = self.get_number_of_symbols_in_bank_string(bits_number=self.bits_number)
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

    def create_empty_hex_files(self, data_banks, ecc_banks=None):
        """

        Create (banks_number) empty hex files
        """
        self.create_dir(self.splitted_files_directory)
        for number in range(data_banks):
            full_banks_name = os.path.join(self.splitted_files_directory,
                                           self.file_name + '_{}{}'.format(number, self.default_ext))

            with open(full_banks_name, 'w'):
                log.info('File {} was created'.format(full_banks_name))

        if ecc_banks:
            for number in range(ecc_banks):
                full_banks_name = os.path.join(self.splitted_files_directory,
                                               self.file_name + '_{}_ECC{}'.format(number, self.default_ext))

                with open(full_banks_name, 'w'):
                    log.info('File {} was created'.format(full_banks_name))
        log.info('All files was created.')