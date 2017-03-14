#!/usr/bin/env python
from re import findall

def get_ecc_and_din_indexes_from_line(verilog_line):

    ecc_index = findall('ECC\[(\d+)\]', verilog_line)[0]

    range_from_string = [int(i) for i in list(findall('\d+:\d+', verilog_line)[0].replace(':', ''))]
    din_range = tuple([i for i in range(range_from_string[1], range_from_string[0] + 1)])

    other_digitals = tuple([int(i) for i in findall('DIN\[(\d+)\]', verilog_line)])

    all_array = din_range + other_digitals

    return int(ecc_index), all_array

def get_ecc_and_din_indexes_from_verilog(verilog):
    result_dict = {}
    for line in verilog.splitlines():
        if 'assign ECC' in line:
            ecc_num, index_list = get_ecc_and_din_indexes_from_line(line)
            result_dict[ecc_num] = index_list

    return result_dict

class PageTree:
    def __init__(self):
        pages = set()

    def __repr__(self):
        return (self.__class__.__name__)

print(PageTree())