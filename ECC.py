from re import findall
from Helpers import create_and_open_file, get_split_file_path, xor, hex_to_bin, bin_to_hex
from DataStorage import DataStorage
from os import path

DEFAULT_ECC = 8


class ECC:
    """
    Split input file

    """

    def __init__(self, file):
        self.hex_file = file
        self.__ECC_file = None
        self.ECC_size = DEFAULT_ECC
        self.ecc_raw = self.get_ecc_and_din_indexes_from_verilog(VERILOG)

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

    def prepare_and_calc_ECC(self, bit_string):
        DIN = bit_string[::-1]  # чтобы в массиве была нужная нумерация
        DIN_bool = [bool(int(item)) for item in DIN]
        ECC_list = list(DIN_bool)

        ECC = self.calc_ecc(ECC_list)
        return ECC


    @property
    def ECC_file(self):
        return self.__ECC_file

    @ECC_file.setter
    def ECC_file(self, new_file):
        self.__ECC_file = new_file


##############################################################
    def generate_ecc_and_write_to_file(self):
        file_with_ecc_name = DataStorage().file_with_ecc = path.join(DataStorage().programm_location,
                                                                     'ECC_from_'+ DataStorage().file_name)
        ecc_file = create_and_open_file(file_with_ecc_name)
        global_adress = DataStorage().start_ecc_address
        global_adress_bin = hex_to_bin(global_adress)
        local_adress_len = 32 - len(str(global_adress_bin))

        with open(self.hex_file, 'r') as f:
            local_adress = 0
            counter = 0
            temp_buffer = ''
            for line in f:
                if counter < 4:
                    # Write new line in the start of buffer because it's more big bits
                    temp_buffer = line.replace('\n', '').replace('\r', '') + temp_buffer
                    counter += 1
                else:
                    local_adress_bin = '{0:0{1}b}'.format(local_adress, local_adress_len)
                    string_for_ecc = global_adress_bin + local_adress_bin + hex_to_bin(temp_buffer)
                    ecc_hex = self.prepare_and_calc_ECC(string_for_ecc)
                    data_for_file = 'adress:{local} '\
                                    'data:{data} '\
                                    'ecc:{ecc}'.format(local=bin_to_hex(local_adress_bin, min_output_lenght=len(local_adress_bin)/4),
                                             data=temp_buffer,
                                             ecc=ecc_hex
                                             )
                    ecc_file.write(data_for_file + '\n')

                    counter = 1
                    temp_buffer = line.replace('\n', '').replace('\r', '')
                    local_adress += 1
        from Logger import log
        log.info('ECC was created in {}'.format(file_with_ecc_name))
        ecc_file.close()

    def calc_ecc(self, bool_list):
        if len(bool_list) != 64:
            raise ValueError('Incorrect input data for calculation ecc!')
        else:
            ecc = [None] * self.ECC_size
            for i, item in self.ecc_raw.items():
                ecc[i] = xor(bool_list, item)

            # prepare ecc to return
            output = []
            for item in ecc:
                # remake bool_ecc to int_ecc, and int_ecc to str_ecc for concatination in output string
                output.append(str(int(item)))
            # change ecc order because hard digital man like a reverse order like [3:0] instead of [0:3]
            return bin_to_hex(''.join(output)[::-1], min_output_lenght=len(output)/4)



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








