#! python3

import openpyxl
import logging
import os
import pprint
from pathlib import Path

import lib.ddl_all
import lib.dml_all

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
            
#start             
logging.debug('program start')

#init
all_scheme = {'EB','EA','EE','EK'}
usr_names = ['dml_usr'] #ここは自由に追加できるようにする
pkg_name = 'dml_pkg' 

#main
logging.debug('-----result-----')


for usr_name in usr_names:
    logging.debug('-- {} --'.format(usr_name))
    for scheme in all_scheme:
        logging.debug('-- {} --'.format(scheme))
        diff_items(getattr(lib, usr_name).all_datas[scheme], lib.dml_pkg.all_datas[scheme]) #dml_usrは変更できるようにgetattrへ
        diff_items(getattr(lib, pkg_name).all_datas[scheme], lib.dml_usr.all_datas[scheme]) #pkgも一応合わせて

#end
logging.debug('program complete')