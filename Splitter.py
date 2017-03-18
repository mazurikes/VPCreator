#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
from Helpers import get_split_file_path, get_file_content

SIZE_OF_ONE_HEX_CHARACTER_IN_BITS = 4


class Splitter:
    """

    Parses input file and splits it.
    """

    def __init__(self, input_file=None, bits_number=32, banks_number=1, ECC_information=None):
        self.input_file = input_file
        self.bits_number = int(bits_number)
        self.banks_number = int(banks_number)

        self.finished_output = []
        self.split_files_path = ''
        self.default_ext = '.vh'

        self.split()

    def split(self):
        self.__create_empty_hex_files()
        self.__write_split_hex_files()

    def __get_size_of_one_string(self):
        with open(self.input_file, 'r', encoding='UTF-8') as f:
            first_string = str(f.readline().replace('\n', ''))
        return len(first_string) * SIZE_OF_ONE_HEX_CHARACTER_IN_BITS

    def __get_number_of_items_in_string(self):
        """
        Get number of items from initial file
        that will be put in one string in new file
        :return:
        """

        bits = int(self.bits_number)
        return int(bits / self.__get_size_of_one_string())

    def __set_finished_output(self):
        file_output = get_file_content(self.input_file)
        items_in_string = self.__get_number_of_items_in_string()

        counter = 0
        temp_str = ''
        for index, item in enumerate(file_output):
            if not counter <= items_in_string - 1:
                self.finished_output.append(temp_str)
                counter = 0
                temp_str = ''
            # Revers adding items in string
            temp_str = item + temp_str
            counter += 1

            if index == len(file_output) - 1:
                self.finished_output.append(temp_str)

    def __write_split_hex_files(self):
        string_number = 0
        self.__set_finished_output()
        list_of_files = []
        list_dir = os.listdir(self.split_files_path)
        file_number = 0

        for file in list_dir:
            list_of_files.append(open(self.split_files_path+file, 'w', encoding='UTF-8'))

        for index, value in enumerate(self.finished_output):
            if not index % self.banks_number:
                if not index:
                    list_of_files[0].write('@{0:<5X}{1}'.format(string_number, value) + '\n')
                    continue
                string_number += 1

            file_number = index % self.banks_number
            list_of_files[file_number].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        # Fill all banks
        if file_number != self.banks_number - 1:
            for index in range(file_number+1, int(self.banks_number)):
                zero_number = 2 * self.__get_number_of_items_in_string()
                value = '0' * zero_number
                list_of_files[index].write('@{0:<5X}{1}'.format(string_number, value) + '\n')

        for file in list_of_files:
            file.close()

    def __create_empty_hex_files(self):
        """

        Create (banks_number) empty hex files
        """

        file_path_list = get_split_file_path(self.input_file)
        if not os.path.exists((file_path_list['directory']+'\\Split hex files')):
            os.mkdir(file_path_list['directory']+'\\Split hex files')
            print('Dir was created')
        else:
            for file in os.listdir(file_path_list['directory']+'\\Split hex files'):
                os.remove(file_path_list['directory']+'\\Split hex files\\{0}'.format(file))
        for number in range(self.banks_number):
            ext = file_path_list['extention'] if file_path_list['extention'] else self.default_ext
            full_name = file_path_list['directory'] + \
                        '\\Split hex files\\' +\
                        file_path_list['file_name'] + \
                        '_' + str(number) + \
                        ext
            with open(full_name, 'w') as f:
                print('File {0} is created'.format(full_name))
        print('All files was created')
        self.split_files_path = file_path_list['directory']+'\\Split hex files\\'


if __name__ == '__main__':
    input_file = 'L:\\Документы\\Python_projects\\Practice\\test_files\\ER_IROM1'
    obj = Splitter(input_file, 32, 4)
    # file_output = obj.get_file_output()
    # print(file_output)
    # print(len(file_output))
    obj.split()
