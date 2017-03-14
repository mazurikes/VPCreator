DEFAULT_ECC = 8

class ECC:
    """
    Split input file

    """

    def __init__(self, start_address, bits=DEFAULT_ECC):
        self.address = start_address
        self.bits = bits
        verilog_file =
        self.pattern = 'DIN\[(.*)\]'

        self.get_ecc_function(verilog_file)

    def get_ecc_function(self, verilog_file):
        from re import findall
        ecc = []
        with open(verilog_file) as f:
            for line in f:
                n
                ecc.append(findall(self.pattern, line))



