from re import findall
from Helpers import create_and_open_file, get_split_file_path, xor

DEFAULT_ECC = 8


class ECC:
    """
    Split input file

    """

    def __init__(self, file):
        self.hex_file = file
        self.__ECC_file = None
        self.length_of_string_for_ECC = 64
        self.ECC_size = DEFAULT_ECC

        self.set_ECC_file_name()
        self.create_bin_file()
        self.create_ECC()

    def create_bin_file(self):
        from Helpers import get_split_file_path
        from Helpers import hex_to_bin
        split_file_path = get_split_file_path(self.hex_file)
        self.input_file_bin = split_file_path['directory'] + '\\' + \
                   split_file_path['file_name'] + \
                   '_bin' + \
                   split_file_path['extention']

        bin_file = open(self.input_file_bin, 'w')

        with open(self.hex_file, 'r', encoding='UTF-8') as f:
            for line in f:
                line = line.replace('\n', '')
                new_line = hex_to_bin((line, ))[0]
                print(line + ': ' + new_line)
                bin_file.write(new_line + '\n')
        bin_file.close()

    def create_ECC(self):
        file = create_and_open_file(self.ECC_file)
        bit_string = ''

        for line in file:
            line.replace('\n', '')
            line_length = len(line)

            dif_with_size = self.length_of_string_for_ECC - len(bit_string)
            if dif_with_size:
                if line_length <= dif_with_size:
                    bit_string = line + bit_string
                else:
                    bit_string = line[line_length - dif_with_size:] + bit_string
                    file.write(bit_string + ': ' + str(self.count_ECC(bit_string)) + '\n')
                    bit_string = line[0:line_length - dif_with_size]
            else:
                file.write(bit_string + ': ' + str(self.count_ECC(bit_string)) + '\n')
                bit_string = line + bit_string
        file.close()

    def set_ECC_file_name(self):
        file_path_list = get_split_file_path(self.hex_file)
        # self.ECC_file = file_path_list['directory'] + '\\Split hex files\\ECC.vh'
        import os
        self.ECC_file = os.path.join(file_path_list['directory'], 'Split hex files', 'ECC.vh')

    def get_ecc_and_din_indexes_from_line(self, verilog_line):

        ecc_index = findall('ECC\[(\d+)\]', verilog_line)[0]

        range_from_string = [int(i) for i in list(findall('\d+:\d+', verilog_line)[0].replace(':', ''))]
        din_range = tuple([i for i in range(range_from_string[1], range_from_string[0] + 1)])

        other_digitals = tuple([int(i) for i in findall('DIN\[(\d+)\]', verilog_line)])

        all_array = din_range + other_digitals

        return int(ecc_index), all_array

    def get_ecc_and_din_indexes_from_verilog(self, verilog):
        result_dict = {}
        for line in verilog.splitlines():
            if 'assign ECC' in line:
                ecc_num, index_list = self.get_ecc_and_din_indexes_from_line(line)
                result_dict[ecc_num] = index_list

        return result_dict

    def calc_ecc(self, bool_list):
        ECC = [None] * self.ECC_size
        ecc_raw = self.get_ecc_and_din_indexes_from_verilog(VERILOG)
        for i, item in ecc_raw.items():
            ECC[i] = xor(bool_list, item)
        return ECC


    def count_ECC(self, bit_string):
        DIN = bit_string[::-1]
        DIN_bool = [bool(int(item)) for item in DIN]
        ECC_list = list(DIN_bool) # чтобы в массиве была нужная нумерация
        ECC = self.calc_ecc(ECC_list)
        return ''.join(ECC)


    @property
    def ECC_file(self):
        return self.__ECC_file

    @ECC_file.setter
    def ECC_file(self, new_file):
        self.__ECC_file = new_file



VERILOG = '''
module ECC_T(DIN, DOUT, ECC);

input  [63:0] DIN;

output [63:0] DOUT;

output [7:0] ECC;

assign DOUT=DIN;

assign ECC[0]=(^DIN[7:0])^DIN[10]^DIN[13]^DIN[14]^DIN[17]^DIN[20]^DIN[23]^DIN[24]^DIN[27]^DIN[35]^DIN[43]^DIN[46]^DIN[47]^DIN[51]^DIN[52]^DIN[53]^DIN[56]^DIN[57]^DIN[58];

assign ECC[1]=(^DIN[15:8])^DIN[0]^DIN[1]^DIN[2]^DIN[18]^DIN[21]^DIN[22]^DIN[25]^DIN[28]^DIN[31]^DIN[32]^DIN[35]^DIN[43]^DIN[51]^DIN[54]^DIN[55]^DIN[59]^DIN[60]^DIN[61];

assign ECC[2]=(^DIN[23:16])^DIN[3]^DIN[4]^DIN[5]^DIN[8]^DIN[9]^DIN[10]^DIN[26]^DIN[29]^DIN[30]^DIN[33]^DIN[36]^DIN[39]^DIN[40]^DIN[43]^DIN[51]^DIN[59]^DIN[62]^DIN[63];

assign ECC[3]=(^DIN[31:24])^DIN[3]^DIN[6]^DIN[7]^DIN[11]^DIN[12]^DIN[13]^DIN[16]^DIN[17]^DIN[18]^DIN[34]^DIN[37]^DIN[38]^DIN[41]^DIN[44]^DIN[47]^DIN[48]^DIN[51]^DIN[59];

assign ECC[4]=(^DIN[39:32])^DIN[3]^DIN[11]^DIN[14]^DIN[15]^DIN[19]^DIN[20]^DIN[21]^DIN[24]^DIN[25]^DIN[26]^DIN[42]^DIN[45]^DIN[46]^DIN[49]^DIN[52]^DIN[55]^DIN[56]^DIN[59];

assign ECC[5]=(^DIN[47:40])^DIN[0]^DIN[3]^DIN[11]^DIN[19]^DIN[22]^DIN[23]^DIN[27]^DIN[28]^DIN[29]^DIN[32]^DIN[33]^DIN[34]^DIN[50]^DIN[53]^DIN[54]^DIN[57]^DIN[60]^DIN[63];

assign ECC[6]=(^DIN[55:48])^DIN[1]^DIN[4]^DIN[7]^DIN[8]^DIN[11]^DIN[19]^DIN[27]^DIN[30]^DIN[31]^DIN[35]^DIN[36]^DIN[37]^DIN[40]^DIN[41]^DIN[42]^DIN[58]^DIN[61]^DIN[62];

assign ECC[7]=(^DIN[63:56])^DIN[2]^DIN[5]^DIN[6]^DIN[9]^DIN[12]^DIN[16]^DIN[15]^DIN[19]^DIN[27]^DIN[35]^DIN[38]^DIN[39]^DIN[43]^DIN[44]^DIN[45]^DIN[48]^DIN[49]^DIN[50];

'''






