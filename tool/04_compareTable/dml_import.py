#! python3

import openpyxl
import logging
import pprint
import os
from pathlib import Path
import lib.ddl_pkg

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


def makeTableData(table_list):
    logging.debug('sheetnames: {}'.format(wb.sheetnames))
    for table_name in table_list & set(wb.sheetnames): #ワークブックのシート名と一致する分だけ
        sheet = wb[table_name]
        scheme = table_name[:2]
                
        for cur_row in range(1, sheet.max_row + 1):
            str = sheet.cell(cur_row, 1).value
            split_str = str.split(",")
            table = split_str[0]
            all_datas[scheme].setdefault(table, {})
            next_sno = all_datas[scheme][table].get('sno',0) + 1
            all_datas[scheme][table]['sno'] = next_sno
            all_datas[scheme][table][next_sno] = {}
            
            for i in range(1, len(split_str)):
                logging.debug('cur_row:{}, i:{}, table:{}, next_sno:{}'.format(cur_row,i,table,next_sno))
                
                #ループの前にリセットしておく
                tmp_column = ''
                tmp_sno = 0
                for tmp_column in lib.ddl_pkg.all_tables[scheme][table]:
                    tmp_sno = lib.ddl_pkg.all_tables[scheme][table][tmp_column]['sno']
                    logging.debug('table:{}, tmp_column:{}, tmp:sno:{}'.format(table,tmp_column,tmp_sno))
                    
                    if i == int(tmp_sno):
                        all_datas[scheme][table][next_sno][tmp_column] = split_str[i]
                        break #見つかったらループを抜け出す。
                    
def add_lib_dml_all(filename, addstr):
    #インポート
    path2export = Path.cwd() / 'lib' /filename
    
    file = open(str(path2export), 'r+')
    addstr_mod = 'import lib.' + addstr
    
    if addstr_mod not in [line.strip() for line in file.readlines()]:
        file.seek(0, os.SEEK_END)
        file.write('\n' + addstr_mod)


#start    
logging.debug('program start')

#init
all_datas = {}
filename= 'dml_*.xlsx' #対象にしたいファイル名orファイル形式を指定
table_list = {'EB_TABLE'
              ,'EA_TABLE'
              ,'EK_TABLE'
              ,'EE_TABLE'}
path2excel = (Path.cwd() / 'excel').glob(filename) #カレントのexcelフォルダを検索対象とする。

#main
for path in path2excel:
    for table in table_list:
        scheme = table[:2]
        all_datas[scheme] = {}
        all_datas[scheme]['name'] = path.stem #拡張子なしはstemを使う
    
    #excel読み込み
    wb = openpyxl.load_workbook(str(path))
    
    #
    makeTableData(table_list)

    file = open('lib/' + path.stem + '.py', 'w')
    file.write('all_datas =' + pprint.pformat(all_datas))
    file.close()
    logging.debug('all_datas: {}'.format(all_datas))
    
    add_lib_dml_all('dml_all.py',path.stem)
    


#end
logging.debug('program complete')