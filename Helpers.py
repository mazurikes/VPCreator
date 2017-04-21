import os
from enum import Enum
from cmath import log
from re import search

HEX_SYMBOL_SIZE_IN_BITS = 4


class MemoryType(Enum):
    WithEcc = 0
    WithoutEcc = 1


class BanksType(Enum):
    Separated = 0
    Joint = 1


class EccLocation(Enum):
    Right = 0
    Left = 1


colors = {'wrong': 'red',
          'empty': 'yellow',
          'correct': 'white'}


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return get_instance


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def xor(boolean_collection, mask):
    result = None
    for num, item in enumerate(boolean_collection):
        if num in mask:
            if result is None:
                result = item
            else:
                result = result ^ item
    return result


def get_split_file_path(file):
    """

    Get item of file path

    File example: L:\\Документы\\Python_projects\\Practice\\test_files\\ER_IROM1.vh
    :return: {
    'directory':'L:\\Документы\\Python_projects\\Practice\\test_files\\',
    'file_name':'ER_IROM1',
    'extention':''
    }

    """

    if os.path.isfile(file):
        directory, file_name_with_extention = os.path.split(file)
        file_name_without_extention, extention = os.path.splitext(file_name_with_extention)
        return {'directory': directory,
                'file_name': file_name_without_extention,
                'extention': extention}
    else:
        raise FileExistsError('File {0} not found'.format(file))


def get_file_content(file):
    """

    Get information from a file
    """

    if os.path.isfile(file):
        with open(file, 'r', encoding='UTF-8') as f:
            file_output = [line.replace('\n', '') for line in f]
        return file_output
    else:
        raise FileExistsError('File {0} not found'.format(file))


def get_ecc(file):
    if os.path.isfile(file):
        with open(file, 'r', encoding='UTF-8') as f:
            file_output = [search(r'ecc:(\w+)', line.replace('\n', '')).group(1) for line in f]
        return file_output
    else:
        raise FileExistsError('File {0} not found'.format(file))


def hex_to_bin(hex_string):
    '''
    Translate hex string to bin string
    :param hex_string:
    :return:
    '''

    new_collection = []
    for item in hex_string:
        new_item = ''
        for char in item:
            int_from_hex = int(char, 16)
            new_item += '{0:04b}'.format(int_from_hex)
        new_collection.append(new_item)
    return ''.join(new_collection)


def bin_to_hex(bin_string, min_output_lenght=None):
    if len(bin_string) % 4 != 0:
        added_zero = len(bin_string) % 4 if bin_string != '0' else 3
        bin_string = '0' * added_zero + bin_string

    hex_string = format(int(bin_string, 2), 'x').upper()

    if min_output_lenght is not None and len(hex_string) < min_output_lenght:
        min_output_lenght = int(min_output_lenght)
        zero_ratio = min_output_lenght - len(hex_string)
        hex_string = '0' * zero_ratio + hex_string
    return hex_string


def create_and_open_file(name):
    return open(name, 'w', encoding='utf-8')


def chunks(string, n):
    'Divides string by n elements'

    output = []
    for i in range(0, len(string), n):
        piece_of_list = string[i:i + n]
        output.append(''.join([str(i) for i in piece_of_list]))
    return output


def get_global_adress_bits(file):
    '''
    Return number of symbol in adress that user has to enter in EccAdressPage
    '''

    try:
        with open(file, 'r', encoding='utf-8') as f:
            number_of_strings =  len(f.read())
    except:
        raise FileExistsError('File {} doesn\'t exist'.format(file))
    else:
        return 32 - log((number_of_strings/4), 2)


def get_number_of_global_adress_symbols(file):
    '''
    It's the very very bad eximple of the function definition
    '''

    def nearest_top_two_power(number):
        from cmath import log
        power = int(log(number, 2).real) + 1
        while power % 4 != 0:
            power += 1
        return power

    try:
        with open(file, 'r', encoding='utf-8') as f:
            output = f.read()
            number_of_strings = len(output.splitlines())
    except:
        raise FileExistsError('File {} doesn\'t exist'.format(file))
    else:
        # Количество бит в этом адресе - это ближайшее к степени двойки сверху число, которым можно закодировать
        # все строки входного файла, учитывая, что тк в исходном файле у нас в строке 8 бит(2 hex), а почему-то
        # длина всего адреса 32 бита, то число, которое введет
        # пользователь = 32 - округлить_к_большей_степени_двойки(количество_слов_в_файле / 4)
        adress_bits = 32 - nearest_top_two_power(number_of_strings / 4)
        return int(adress_bits / 4)




