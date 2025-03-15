#! python3

import openpyxl
import logging
import os
import pprint
import sys
import json
from pathlib import Path
from datetime import datetime
import importlib

# import lib.ddl_pkg
# import lib.ddl_usr


logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

def minus_items(t1, t2):
    #table <t1-t2>
    for table in (t1.keys() - t2.keys()):
        # logging.debug('t1:{}'.format(t1))
        logging.info('minus - table<{}-{}>: {}'.format(t1['name'],t2['name'],table))
    
    #column <t1-t2>
    for table in t1.keys() & t2.keys() - set(['name']): #all_tablesにnameを無理やり入れたので除外しとく
        for column in t1[table].keys() - t2[table].keys():
            logging.info('minus - column<{}-{}>: {}/{}'.format(t1['name'], t2['name'], table, column))

def diff_items(t1, t2): 
    #column <t1 diff t2>
    for table in t1.keys() & t2.keys() - set(['name']): #all_tablesにnameを無理やり入れたので除外しとく
        for column in t1[table].keys() & t2[table].keys():
            t1_type = t1[table][column]['type']
            t1_len = t1[table][column]['len']
            t2_type = t2[table][column]['type']
            t2_len = t2[table][column]['len']

            if t1_type != t2_type:
                logging.info('diff - {}/{}/{} - {}:{}, {}:{}'.format(table, column, 'type', t1['name'], t1_type, t2['name'], t2_type))
            
            if t1_len != t2_len:
                logging.info('diff - {}/{}/{} - {}:{}, {}:{}'.format(table, column, 'len', t1['name'], t1_len, t2['name'], t2_len))                

def writelog():
    #ログファイル
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    logfilename = 'result_' + now + '.log'
    path_to_logdir.mkdir(parents=True, exist_ok=True)

    path_to_logfile = path_to_logdir / logfilename

    file_handler = logging.FileHandler(path_to_logfile, encoding='utf-8')
    logging.getLogger().addHandler(file_handler)

def import_lib():
    if str(path_to_libdir) not in sys.path:
        sys.path.insert(0, str(path_to_libdir))

    m1 = importlib.import_module(pkg_name)
    m2 = importlib.import_module(usr_name)

    return (m1, m2)

    

logging.info('program start ...')


if len(sys.argv) > 1:
    json_str = sys.argv[1]
    data = json.loads(json_str)
    logging.info(f'受け取ったjson: {data}')
    
    pkg_name = data['pkg_name']
    usr_name = data['usr_name']
    all_scheme = data['gyomu_cd']
    path_to_logdir = Path(data['path_to_log'])
    path_to_libdir = Path(data['path_to_lib']) / 'ddl'
    
else:
    logging.info(f'引数が渡されていません。プログラムを終了します。')
    sys.exit()

writelog()
(module_pkg, module_usr) = import_lib()

for scheme in all_scheme:
    logging.debug('-- {} --'.format(scheme))
    minus_items(module_pkg.all_tables[scheme], module_usr.all_tables[scheme])
    minus_items(module_usr.all_tables[scheme], module_pkg.all_tables[scheme])
    diff_items(module_usr.all_tables[scheme], module_pkg.all_tables[scheme])
logging.debug('program complete')