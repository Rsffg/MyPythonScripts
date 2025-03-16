#! python3

import openpyxl
import logging
import os
import pprint
from pathlib import Path
import sys
import json
import importlib
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')



def diff_items(t1, t2): 
    for table in t1.keys() - t2.keys():
        logging.debug('minus - table<{}-{}>: {}'.format(t1['name'],t2['name'],table))        
        
    #column <t1 diff t2>
    for table in t1.keys() & t2.keys() - set(['name']): #all_tablesにnameを無理やり入れたので除外しとく
        for sno in t1[table].keys():
            datas = t1[table][sno]
            if datas not in t2[table].values():
                logging.debug('diff - {} - table:{}/{}/{}'.format(t1['name'], table, sno, datas))

def get_mylib_mobule(name):
    if str(path_to_lib) not in sys.path:
        sys.path.insert(0, str(path_to_lib))

    return importlib.import_module(name)

def writelog():
    #ログファイル
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    logfilename = 'result_dml_' + now + '.log'
    path_to_log.mkdir(parents=True, exist_ok=True)

    path_to_logfile = path_to_log / logfilename

    file_handler = logging.FileHandler(path_to_logfile, encoding='utf-8')
    logging.getLogger().addHandler(file_handler)
    
#start             
logging.debug('program start')

if len(sys.argv) > 1:
    json_str = sys.argv[1]
    data = json.loads(json_str)
    logging.debug(f'受け取ったjson: {data}')
    
    #セット
    path_to_lib = Path(data['path_to_lib'])
    path_to_log = Path(data['path_to_log'])
    all_scheme = set(data['gyomu_cd'])
    usr_name = data['usr_name']
    pkg_name = data['pkg_name']


#main
logging.debug('-----result-----')

pkg_dml_module = get_mylib_mobule('dml.' + pkg_name)
usr_dml_module = get_mylib_mobule('dml.' + usr_name)

writelog()

logging.debug('-- {} --'.format(usr_name))
for scheme in all_scheme:
    logging.debug('-- {} --'.format(scheme))
    diff_items(usr_dml_module.all_datas[scheme], pkg_dml_module.all_datas[scheme]) 
    diff_items(pkg_dml_module.all_datas[scheme], usr_dml_module.all_datas[scheme]) 

#end
logging.debug('program complete')