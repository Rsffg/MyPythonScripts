#! python3

import openpyxl
import logging
import pprint
import os
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


def makeTableData(table_list):
    logging.debug('sheetnames: {}'.format(wb.sheetnames))
    for table_name in table_list & set(wb.sheetnames): #ワークブックのシート名と一致する分だけ
        sheet = wb[table_name]
        scheme = table_name[:2]
        
        #連番用
        pre_table =''
        sno=1
        
        for cur_row in range(1, sheet.max_row + 1):
            table = sheet.cell(cur_row, 1).value
            col = sheet.cell(cur_row, 2).value
            type = sheet.cell(cur_row, 3).value
            len = sheet.cell(cur_row, 4).value
            
            if table != pre_table:
                sno = 1
            
            logging.debug('scheme: {}, table: {}, col: {}, type: {}, len: {}, sno: {}'.format(scheme, table, col, type, len, sno))
            
            all_tables[scheme].setdefault(table, {})
            all_tables[scheme][table].setdefault(col, {'type': type, 'len': len, 'sno':sno})
            
            pre_table = table
            sno += 1

def add_lib_ddl_all(filename, add_str):
    path_lo = Path.cwd() / 'lib' / filename
    
    file_lo = open(str(path_lo), 'r+')
    add_str_mod = 'import lib.' + add_str
    
    file_lo.seek(0) #readlines()は、現在の位置から読み取るので念の為offsecを0にしておく
    if add_str_mod not in [line.strip() for line in file_lo.readlines()]:
        file_lo.seek(0, os.SEEK_END)
        file_lo.write(add_str_mod + '\n')

#start
logging.debug('program start')

#init
all_tables = {}
filename='ddl_*.xlsx'
table_list = {'EB_TABLE'
              ,'EA_TABLE'
              ,'EK_TABLE'
              ,'EE_TABLE'}
path2excel = (Path.cwd() / 'excel').glob(filename) #カレントのexcelフォルダを検索対象とする。

#main
for path in path2excel:
    for table in table_list:
        scheme = table[:2]
        all_tables[scheme] = {}
        all_tables[scheme]['name'] = path.stem

    wb = openpyxl.load_workbook(str(path))
    makeTableData(table_list)
    
    file = open('lib/' + path.stem + '.py', 'w')
    file.write('all_tables =' + pprint.pformat(all_tables))
    file.close()
    
    #第1引数に追加するファイル名を、第2引数に追加する文字を指定する
    add_lib_ddl_all('ddl_all.py', path.stem)

#end
logging.debug('program complete')