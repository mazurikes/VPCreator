import os


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return get_instance


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


def hex_to_bin(collection):
    new_collection = []
    for item in collection:
        new_item = ''
        for char in item:
            int_from_hex = int(char, 16)
            new_item += '{0:04b}'.format(int_from_hex)
        new_collection.append(new_item)
    return new_collection


def create_and_open_file(name):
    return open(name, 'w')

