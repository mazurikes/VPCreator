SIZE_OF_ONE_HEX_CHARACTER_IN_BITS = 4
FILE = 'L:\\test_files\\ER_IROM1'
BITS_NUMBER = 4


def get_number_of_symbols_in_input_file_string():
    with open(FILE, 'r', encoding='UTF-8') as f:
        first_string = str(f.readline().replace('\n', ''))
    return len(first_string)


def get_number_of_symbols_in_bank_string():
    return BITS_NUMBER / SIZE_OF_ONE_HEX_CHARACTER_IN_BITS


def make_result_list():
    from Helpers import get_file_content
    file_content = get_file_content(FILE)
    result_list = []

    symbols_in_file_string = get_number_of_symbols_in_input_file_string()
    symbols_in_bank_string = get_number_of_symbols_in_bank_string()
    number_of_input_string_in_bank_string = int(symbols_in_bank_string / symbols_in_file_string)

    temp_string = ''
    counter = 0
    for index, string in enumerate(file_content):
        if counter < number_of_input_string_in_bank_string:
            temp_string = string + temp_string
            counter += 1
        else:
            result_list.append(temp_string)
            temp_string = ''
            counter = 0
    print(result_list)
    return result_list


def set_finished_output():
    from Helpers import get_file_content
    file_content = get_file_content(FILE)
    finished_output = []

    # Number of items(hex symbols) in string for new files
    items_in_string = get_number_of_items_in_string()
    print('in string {}'.format(items_in_string))

    counter = 0
    temp_str = ''
    for index, item in enumerate(file_content):
        if not counter <= items_in_string - 1:
            finished_output.append(temp_str)
            counter = 0
            temp_str = ''
        # Revers adding items in string
        temp_str = item + temp_str
        counter += 1

        if index == len(file_content) - 1:
            finished_output.append(temp_str)
    print(finished_output)

make_result_list()

