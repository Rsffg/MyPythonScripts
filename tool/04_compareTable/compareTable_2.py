#! python3

import openpyxl
import logging
import os
import pprint

import pkg
import usr

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.debug('program start')

def minus_items(t1, t2):
    #table <t1-t2>
    for table in (t1.keys() - t2.keys()):
        # logging.debug('t1:{}'.format(t1))
        logging.debug('minus - table<{}-{}>: {}'.format(t1['name'],t2['name'],table))
    
    #column <t1-t2>
    for table in t1.keys() & t2.keys() - set(['name']): #all_tablesにnameを無理やり入れたので除外しとく
        for column in t1[table].keys() - t2[table].keys():
            logging.debug('minus - column<{}-{}>: {}/{}'.format(t1['name'], t2['name'], table, column))

def diff_items(t1, t2): 
    #column <t1 diff t2>
    for table in t1.keys() & t2.keys() - set(['name']): #all_tablesにnameを無理やり入れたので除外しとく
        for column in t1[table].keys() & t2[table].keys():
            t1_type = t1[table][column]['type']
            t1_len = t1[table][column]['len']
            t2_type = t2[table][column]['type']
            t2_len = t2[table][column]['len']

            if t1_type != t2_type:
                logging.debug('diff - {}/{}/{} - {}:{}, {}:{}'.format(table, column, 'type', t1['name'], t1_type, t2['name'], t2_type))
            
            if t1_len != t2_len:
                logging.debug('diff - {}/{}/{} - {}:{}, {}:{}'.format(table, column, 'len', t1['name'], t1_len, t2['name'], t2_len))                


#column  pkg - usr
logging.debug('-----result-----')

all_scheme = {'EB','EA','EE','EK'}

for scheme in all_scheme:
    logging.debug('-- {} --'.format(scheme))
    minus_items(pkg.all_tables[scheme], usr.all_tables[scheme])
    minus_items(usr.all_tables[scheme], pkg.all_tables[scheme])
    diff_items(usr.all_tables[scheme], pkg.all_tables[scheme])
logging.debug('program complete')