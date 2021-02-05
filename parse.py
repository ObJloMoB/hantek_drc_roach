import os
import csv
import struct
import configparser

import xlsxwriter
from pprint import pprint

DEF_CFG = {'HEADER_SIZE': 760,
           'NUM_CH': 8}


class Parser:
    def __init__(self, cfg_p):
        self.cfg = self.read_cfg(cfg_p)
        self.drc_data = None

    def read_cfg(self, cfg_p):
        cfg = configparser.ConfigParser()

        cfg.read(cfg_p)

        print(cfg)

        for k, v in DEF_CFG.items():
            print(k)
            if k not in cfg['BASE'].keys():
                cfg['BASE'][k] = str(v)
        return cfg

    def parse(self):
        file = open(self.cfg['BASE']['DRC_SOURCE'], 'rb')

        head_sz = int(self.cfg['BASE']['HEADER_SIZE'])
        header_b = file.read(4*head_sz)
        header = struct.unpack('<'+'i'*head_sz,
                               header_b)

        self.drc_data = []
        while True:
            num_b = file.read(2)
            if num_b:
                num = struct.unpack('<'+'h', num_b)
                if num[0]:
                    useless = file.read(2*3)

                    print('NUM')
                    print(num)

                    data_b = file.read(2*num[0])
                    data = struct.unpack('<'+'h'*num[0], data_b)
                    self.drc_data.append(data)
                else:
                    print('Eating spacer')
                    continue
            else:
                break

        print('data left', len(file.read()))
        file.close()

    def check_save_fld(self):
        print('Check save folder exists')
        save_dir = os.path.dirname(self.cfg['BASE']['DEST'])
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            print('Created folder')
        else:
            print('Ok it is already there')

    def save_csv(self):
        self.check_save_fld()

        print('Start saving to CSV')
        num_ch = int(self.cfg['BASE']['NUM_CH'])
        with open(self.cfg['BASE']['DEST'], 'w', newline='') as csv_f:
            csv_writer = csv.writer(csv_f,
                                    delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)

            row = [f'chan_{x}' for x in range(num_ch)]
            csv_writer.writerow(row)

            for i in range(len(self.drc_data)//num_ch):
                cols = self.drc_data[i*num_ch:(i+1)*num_ch]

                for j in range(len(cols[0])):
                    row = [cols[x][j] for x in range(num_ch)]
                    csv_writer.writerow(row)
        print('Saving done. You can leave me be')

    def save_xls(self):
        self.check_save_fld()

        print('Start saving to XLSX')
        workbook = xlsxwriter.Workbook(self.cfg['BASE']['DEST'])
        worksheet = workbook.add_worksheet()

        num_ch = int(self.cfg['BASE']['NUM_CH'])

        row = [f'chan_{x}' for x in range(num_ch)]
        worksheet.write_row(0, 0, row)

        for i in range(len(self.drc_data)//num_ch):
            cols = self.drc_data[i*num_ch:(i+1)*num_ch]

            for j in range(len(cols[0])):
                row = [cols[x][j] for x in range(num_ch)]
                worksheet.write_row(i*len(cols[0]) + j + 1, 0, row)

        workbook.close()
        print('Saving done. You can leave me be')


if __name__ == '__main__':
    try:
        psr = Parser('config.ini')
        psr.parse()
        psr.save_xls()
    except Exception as e:
        print('We have a problem')
        print(e)

    input('Just read logs and press ENTER')
