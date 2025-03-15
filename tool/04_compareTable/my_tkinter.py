
import logging.config
from pathlib import Path
import openpyxl
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import subprocess
import logging
import json
import re

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s ')

class MyUtil:
    # json_text = ''
    
    # @classmethod
    # def create_buttons(cls, json_text):
    #     buttons = [
    #     ('1.インポート(DDL)', lambda: MyUtil.run_script('ddl_import.py', json_text)),
    #     ('2.比較(DDL)', lambda: MyUtil.run_script('ddl_compare.py')),
    #     ('3.インポート(DML)', lambda: MyUtil.run_script('dml_import.py')),
    #     ('4.比較(DDL)', lambda: MyUtil.run_script('dml_compare.py')),
    #     ]
    
    @classmethod
    def run_script(cls, script_name, json_str=''):
        path_to_script = Path(__file__).parent / script_name
        logging.debug(f'実行するスクリプト: {path_to_script}')
        subprocess.run(['python', str(path_to_script), json_str])    
    

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #root
        self.title('app-test')
        self.geometry('600x800')
        
        #nootbook
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.ddl_tab = tk.Frame(notebook)
        self.dml_tab = tk.Frame(notebook)
        self.setting_tab = tk.Frame(notebook)
        
        notebook.add(self.ddl_tab, text='DDL')
        notebook.add(self.setting_tab, text='設定')
        notebook.add(self.dml_tab, text='DML')
        
        #SETTING TAB
        ttk.Label(self.setting_tab, text='設定画面').pack()
        SettingFrame(self.setting_tab).pack()
        
        #DDL TAB
        self.first_frame = DDLImportFrame(self.ddl_tab)
        self.last_frame = LastFrame(self.ddl_tab)
        self.second_frame = DDLCompareFrame(self.ddl_tab)
        
        #DML TAB
        ttk.Label(self.dml_tab, text='DMLの取込・比較を行う画面です。').pack(side='top', fill='x', pady=10)
        DMLImportFrame(self.dml_tab).pack(side='top', fill='x', pady=10)
        DMLCompareFrame(self.dml_tab).pack(side='top', fill='x', pady=10)
        
        self.first_frame.pack(side='top', fill='x', pady=10)
        self.second_frame.pack(side='top', fill='x', pady=10)
        self.last_frame.pack(side='bottom', fill='x', pady=10)
    
        

class DDLImportFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove',bg='lightblue')
        
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        
        tk.Label(self, text='1.インポート(DDL)').grid(row=0, column=0, columnspan=3, sticky='w')
        tk.Message(self, text='フォルダ名', width=80).grid(row=1, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_excel, width=400).grid(row=1, column=1, columnspan=3, sticky='w')
        tk.Message(self, text='ファイル名', width=80).grid(row=2, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_excel_ddl_filename, width=500).grid(row=2, column=1, columnspan=3, sticky='w')
        
        tk.Button(self, text='取込みファイル確認', command=self.check_path).grid(row=10, column=0, sticky='e')
        self.filelist = tk.Listbox(self, height=5)
        self.filelist.grid(row=10, column=1, sticky='w')
        
        tk.Button(self, text='取込み資産確認', command=self.check_targetassets).grid(row=20, column=0, sticky='e')
        self.assetslist = tk.Listbox(self, height=5)
        self.assetslist.grid(row=20, column=1, sticky='w')

        tk.Button(self, text='取込', command=self.exec_ddl_import).grid(row=100, column=0, sticky='e')

    def exec_ddl_import(self):
        logging.debug('取込み開始しました')
        data = {}
        
        list = self.assetslist.get(0, tk.END)
        if not list:
            logging.info('取込み資産が空です.処理を中断します。')
            return

        #setting
        data['path_to_excel'] = SettingFrame.text_var_excel.get()
        data['path_to_lib'] = SettingFrame.text_var_lib.get()
        data['filename'] = SettingFrame.text_var_excel_ddl_filename.get()
        data['target'] = list #直前で拾ったやつ
        data['regex'] = SettingFrame.text_var_regex.get()
        
        json_str = json.dumps(data)
        logging.debug('run_scriptを実行します')
        MyUtil.run_script('ddl_import.py', json_str)
        logging.debug('run_scriptは終了しました')

    
    def check_path(self):
        logging.debug('取込み確認ボタンを開始します')
        path_to_excel = Path(SettingFrame.text_var_excel.get()).glob(SettingFrame.text_var_excel_ddl_filename.get())
        logging.debug(f'取込み予定ファイル: {path_to_excel}')
        
        self.filelist.delete(0, tk.END) #リストをクリア
        for path in path_to_excel:
            self.filelist.insert(tk.END, path.name)
        logging.debug('取込み確認ボタンを終了します')

    def check_targetassets(self):
        logging.debug('資産確認ボタンが押されました。')
        print(SettingFrame.text_var_targetcode.get().split('/'))
        print(SettingFrame.text_var_targetassets.get().split('/'))
        
        assets = SettingFrame.text_var_targetassets.get().split('/')
        codes = SettingFrame.text_var_targetcode.get().split('/')
        joint = '_' #とりまリテラル

        self.assetslist.delete(0, tk.END)
        for a in assets:
            for c in codes:
                str = c + joint + a
                self.assetslist.insert(tk.END, str)
                    
    def select_file_path(self):
        file_path = filedialog.askopenfilename(initialdir=Path.cwd())
        if file_path:
            logging.info(f'選択されたファイル:{file_path}')
            
            self.text_var_filename.set(file_path)
            
    def select_directory_path(self):
        dir_path = filedialog.askdirectory(initialdir=Path.cwd())
        if dir_path:
            logging.info(f'選択されたディレクトリ:{dir_path}')
            self.text_var_excle.set(dir_path)

class DDLCompareFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove')
        
        #title
        tk.Message(self, text='2.比較(DDL)', width=1000).grid(row=0, column=0, columnspan=3, sticky='w')

        tk.Message(self, text='libフォルダ名', width=80).grid(row=1, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_lib, width=400).grid(row=1, column=1, columnspan=3, sticky='w')
        
        #比較対象1:pkg
        tk.Message(self, text='比較対象1(pkg): ', width=200).grid(row=3, column=0, sticky='ew')
        tk.Message(self, textvariable=SettingFrame.text_var_pkg_name, width=500).grid(row=3, column=1, sticky='w')
        
        #比較対象2:usr
        tk.Message(self, text='比較対象2(usr): ',  width=200).grid(row=4, column=0, sticky='ew')
        tk.Message(self, textvariable=SettingFrame.text_var_usr_name, width=500).grid(row=4, column=1, sticky='w')
        
        tk.Button(self, text='実行', command=self.exec_ddl_compare).grid(row=20,column=1)
            
    def exec_ddl_compare(self):
        data = {}
        
        gyomu_cd = tuple(SettingFrame.text_var_targetcode.get().split('/'))
        print(gyomu_cd, type(gyomu_cd))
        
        #setting
        data['pkg_name'] = SettingFrame.text_var_pkg_name.get()
        data['usr_name'] = SettingFrame.text_var_usr_name.get()
        data['gyomu_cd'] = gyomu_cd
        data['path_to_log'] = SettingFrame.text_var_log.get()
        data['path_to_lib'] = SettingFrame.text_var_lib.get()
        
        json_str = json.dumps(data)
        logging.debug('run_scriptを実行します')
        MyUtil.run_script('ddl_compare.py', json_str)        
        logging.debug('run_scriptは終了しました')

class DMLImportFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove',bg='lightblue')
        
        # gridのweight=1にして、余白分を拡張
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        
        #ヘッダ
        tk.Label(self, text='1.インポート(DML)').grid(row=0, column=0, columnspan=3, sticky='w')
        
        #エクセルフォルダの確認
        tk.Label(self, text='フォルダ名').grid(row=1, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_excel, width=400).grid(row=1, column=1, columnspan=3, sticky='w')
        
        #エクセルファイルの確認
        tk.Label(self, text='ファイル名').grid(row=2, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_excel_dml_filename, width=500).grid(row=2, column=1, columnspan=3, sticky='w')
        
        tk.Button(self, text='取込みファイル確認', command=self.check_libpath).grid(row=10, column=0, sticky='e')
        self.filelist = tk.Listbox(self, height=5)
        self.filelist.grid(row=10, column=1, sticky='w')
        
        tk.Button(self, text='取込み資産確認', command=self.check_targetassets).grid(row=20, column=0, sticky='e')
        self.assetslist = tk.Listbox(self, height=5)
        self.assetslist.grid(row=20, column=1, sticky='w')

        tk.Button(self, text='取込', command=self.exec_dml_import).grid(row=100, column=0, sticky='e')

    def exec_dml_import(self):
        logging.debug('取込み開始しました')
        data = {}
        
        list = self.assetslist.get(0, tk.END)
        if not list:
            logging.info('取込み資産が空です.処理を中断します。')
            return

        #setting
        data['path_to_excel'] = SettingFrame.text_var_excel.get()
        data['path_to_lib'] = SettingFrame.text_var_lib.get()
        data['filename'] = SettingFrame.text_var_excel_dml_filename.get()
        data['target'] = list #直前で拾ったやつ
        data['regex'] = SettingFrame.text_var_regex.get()
        
        json_str = json.dumps(data)
        logging.debug('run_scriptを実行します')
        MyUtil.run_script('dml_import.py', json_str)
        logging.debug('run_scriptは終了しました')

    
    def check_libpath(self):
        path_to_excel = Path(SettingFrame.text_var_excel.get()).glob(SettingFrame.text_var_excel_dml_filename.get())
        logging.debug(f'path_to_lib: {path_to_excel}')
        
        self.filelist.delete(0, tk.END) #リストをクリア
        for path in path_to_excel:
            self.filelist.insert(tk.END, path.name)

    def check_targetassets(self):
        logging.debug('資産確認ボタンが押されました。')
        print(SettingFrame.text_var_targetcode.get().split('/'))
        print(SettingFrame.text_var_targetassets.get().split('/'))
        
        assets = SettingFrame.text_var_targetassets.get().split('/')
        codes = SettingFrame.text_var_targetcode.get().split('/')
        joint = '_' #とりまリテラル

        self.assetslist.delete(0, tk.END)
        for a in assets:
            for c in codes:
                str = c + joint + a
                self.assetslist.insert(tk.END, str)
                    
    def select_file_path(self):
        file_path = filedialog.askopenfilename(initialdir=Path.cwd())
        if file_path:
            logging.info(f'選択されたファイル:{file_path}')
            
            self.text_var_filename.set(file_path)
            
    def select_directory_path(self):
        dir_path = filedialog.askdirectory(initialdir=Path.cwd())
        if dir_path:
            logging.info(f'選択されたディレクトリ:{dir_path}')
            self.text_var_excle.set(dir_path)

class DMLCompareFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove')
        
        #title
        tk.Message(self, text='2.比較(DDL)', width=1000).grid(row=0, column=0, columnspan=3, sticky='w')

        tk.Message(self, text='libフォルダ名', width=80).grid(row=1, column=0)
        tk.Message(self, textvariable=SettingFrame.text_var_lib, width=400).grid(row=1, column=1, columnspan=3, sticky='w')
        
        self.filelist = tk.Listbox(self, height=5)
        self.filelist.grid(row=10, column=1)
        
        #比較対象1:pkg
        tk.Message(self, text='比較対象1(pkg): ', width=200).grid(row=3, column=0, sticky='ew')
        tk.Message(self, textvariable=SettingFrame.text_var_pkg_name, width=500).grid(row=3, column=1, sticky='w')
        
        #比較対象2:usr
        tk.Message(self, text='比較対象2(usr): ',  width=200).grid(row=4, column=0, sticky='ew')
        tk.Message(self, textvariable=SettingFrame.text_var_usr_name, width=500).grid(row=4, column=1, sticky='w')
        
        tk.Button(self, text='事前確認', command=self.check_libpath).grid(row=10, column=0, sticky='e')
        tk.Button(self, text='実行', command=self.exec_ddl_compare).grid(row=20,column=1)

    def check_libpath(self):
        path_to_lib = Path(SettingFrame.text_var_lib.get()).glob('*.py')
        print(str(path_to_lib))
        
        for path in path_to_lib:
            self.filelist.insert(tk.END, path.stem)
            
    def exec_ddl_compare(self):
        data = {}
        
        gyomu_cd = tuple(SettingFrame.text_var_targetcode.get().split('/'))
        print(gyomu_cd, type(gyomu_cd))
        
        #setting
        data['pkg_name'] = SettingFrame.text_var_pkg_name.get()
        data['usr_name'] = SettingFrame.text_var_usr_name.get()
        data['gyomu_cd'] = gyomu_cd
        data['path_to_log'] = SettingFrame.text_var_log.get()
        data['path_to_lib'] = SettingFrame.text_var_lib.get()
        
        json_str = json.dumps(data)
        logging.debug('run_scriptを実行します')
        MyUtil.run_script('ddl_compare.py', json_str)        
        logging.debug('run_scriptは終了しました')

class SettingFrame(tk.Frame):
    text_var_excel = None
    text_var_lib = None
    text_var_lib_filename = None
    text_var_setting = None
    text_var_excel_ddl_filename = None
    text_var_excel_dml_filename = None
    text_var_pkg_name = None
    text_var_dml_pkg_name = None
    text_var_usr_name = None
    text_var_dml_usr_name = None
    text_var_regex = None
    text_var_targetcode = None
    text_var_targetassets = None,
    text_var_log = None
    
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove',bg='lightblue')
        
        
        #Excel path
        SettingFrame.text_var_excel = tk.StringVar()
        tk.Label(self, text='excelパス(共通)').grid(row=0, column=0, sticky='w', columnspan=3)
        tk.Button(self, text='フォルダー選択', command=lambda: self.select_dir_path(SettingFrame.text_var_excel)).grid(row=0, column=1, sticky='w')
        entry_excel = tk.Entry(self, textvariable=SettingFrame.text_var_excel, width=50).grid(row=2, column=0, columnspan=3, sticky='w')
        
        #Excel ddl filename
        SettingFrame.text_var_excel_ddl_filename = tk.StringVar()
        tk.Label(self, text='excelファイル名(DDL)').grid(row=5, column=0, sticky='w', columnspan=3)
        entry_excel = tk.Entry(self, textvariable=SettingFrame.text_var_excel_ddl_filename, width=20).grid(row=6, column=0, columnspan=2, sticky='w')
        
        #Excel dml filename
        SettingFrame.text_var_excel_dml_filename = tk.StringVar()
        tk.Label(self, text='excelファイル名(DML)').grid(row=5, column=1, sticky='w', columnspan=3)
        entry_excel = tk.Entry(self, textvariable=SettingFrame.text_var_excel_dml_filename, width=20).grid(row=6, column=1, columnspan=2, sticky='w')
        
        #lib path
        SettingFrame.text_var_lib = tk.StringVar()
        tk.Label(self, text='libパス').grid(row=10, column=0, sticky='w', columnspan=3)
        tk.Button(self, text='フォルダー選択', command=lambda: self.select_dir_path(SettingFrame.text_var_lib)).grid(row=10, column=1, sticky='w')
        tk.Entry(self, textvariable=SettingFrame.text_var_lib, width=50).grid(row=11, column=0, columnspan=3, sticky='w')
        
        SettingFrame.text_var_lib_filename = tk.StringVar()
        tk.Label(self, text='libファイル名').grid(row=12, column=0, sticky='w', columnspan=3)
        tk.Entry(self, textvariable=SettingFrame.text_var_lib_filename, width=20).grid(row=13, column=0, columnspan=3, sticky='w')
        
        #setting path
        SettingFrame.text_var_setting = tk.StringVar()
        SettingFrame.text_var_setting.set(Path(__file__).parent / 'setting')
        tk.Label(self, text='設定ファイルのパス').grid(row=30, column=0, sticky='w', columnspan=3)
        tk.Button(self, text='フォルダー選択', command=lambda: self.select_dir_path(SettingFrame.text_var_setting)).grid(row=30, column=1, sticky='w')
        entry_excel = tk.Entry(self, textvariable=SettingFrame.text_var_setting, width=50).grid(row=31, column=0, columnspan=3, sticky='w')
        
        #正規表現
        SettingFrame.text_var_regex = tk.StringVar()
        tk.Label(self, text='正規表現').grid(row=35, column=0, sticky='w', columnspan=3)
        tk.Entry(self, textvariable=SettingFrame.text_var_regex).grid(row=36, column=0, columnspan=2, sticky='w')
        
        #団体一覧
        tk.Label(self, text='団体一覧').grid(row=40, column=0, sticky='w', columnspan=3)
        self.usrlist = tk.Listbox(self, height=3)
        self.usrlist.grid(row=41, column=0, columnspan=2, sticky='w', rowspan=3)
        tk.Button(self, text='一覧取得', command=self.get_usrnames).grid(row=40, column=1)
        tk.Button(self, text='pkg決定', command=lambda: self.set_name('pkg')).grid(row=41, column=1)
        tk.Button(self, text='usr決定', command=lambda: self.set_name('usr')).grid(row=42, column=1)
        
        #団体A
        SettingFrame.text_var_pkg_name = tk.StringVar()
        tk.Label(self, text='pkg').grid(row=50, column=0, sticky='w', columnspan=3)
        tk.Entry(self, textvariable=SettingFrame.text_var_pkg_name).grid(row=51, column=0, sticky='w')
        
        
        #団体B
        SettingFrame.text_var_usr_name = tk.StringVar()
        tk.Label(self, text='usr').grid(row=50, column=1, sticky='w', columnspan=3)
        tk.Entry(self, textvariable=SettingFrame.text_var_usr_name).grid(row=51, column=1, sticky='w')
        
        
        #調査対象業務
        SettingFrame.text_var_targetcode = tk.StringVar()
        tk.Label(self, text='調査対象業務').grid(row=60, column=0, sticky='w')
        tk.Entry(self, textvariable=SettingFrame.text_var_targetcode).grid(row=61, column=0, sticky='w')
        
        #調査対象資産
        SettingFrame.text_var_targetassets = tk.StringVar()
        tk.Label(self, text='調査対象資産').grid(row=70, column=0, sticky='w')
        tk.Entry(self, textvariable=SettingFrame.text_var_targetassets).grid(row=71, column=0, sticky='w')
        
        #ログファイル出力先,
        SettingFrame.text_var_log = tk.StringVar()
        tk.Label(self, text='ログフォルダ').grid(row=80, column=0, sticky='w'),
        tk.Button(self, text='フォルダ選択', command=lambda: self.select_dir_path(SettingFrame.text_var_log)).grid(row=80, column=1),
        tk.Entry(self, textvariable=SettingFrame.text_var_log).grid(row=81, column=0, sticky='w')
        
        
        
        #データの読み込み
        self.load_setting_data()
        
        #保存ボタン
        tk.Button(self, text='保存', command=self.save_setting_data).grid(row=100, column=2)

        #読込ボタン
        tk.Button(self, text='読込', command=self.load_setting_data).grid(row=100, column=1)
        
    def select_dir_path(self, text_var):
        dir_path = filedialog.askdirectory(initialdir=Path.cwd())
        if dir_path:
            logging.info(f'選択されたディレクトリ:{dir_path}')
            text_var.set(dir_path)
    
    def save_setting_data(self):
        logging.debug('保存ボタンが押されました')
        path_to_setting = Path(SettingFrame.text_var_setting.get()) / 'settings.json'
        print(path_to_setting)
        data = {
            'text_var_excel': SettingFrame.text_var_excel.get(),
            'text_var_lib': SettingFrame.text_var_lib.get(),
            'text_var_excel_ddl_filename': SettingFrame.text_var_excel_ddl_filename.get(),
            'text_var_excel_dml_filename': SettingFrame.text_var_excel_dml_filename.get(),
            'text_var_lib_filename': SettingFrame.text_var_lib_filename.get(),
            'text_var_lib_filename': SettingFrame.text_var_lib_filename.get(),
            'text_var_regex': SettingFrame.text_var_regex.get(),
            'text_var_pkg_name': SettingFrame.text_var_pkg_name.get(),
            'text_var_usr_name': SettingFrame.text_var_usr_name.get(),
            'text_var_targetcode': SettingFrame.text_var_targetcode.get(),
            'text_var_targetassets': SettingFrame.text_var_targetassets.get(),
            'text_var_log': SettingFrame.text_var_log.get()
        }
        with open(path_to_setting, 'w') as f:
            json.dump(data, f)
            # pass
        
        print('設定を保存しました。')
    
    def load_setting_data(self):
        logging.debug('読込ボタンが押されました。')
        path_to_setting = Path(SettingFrame.text_var_setting.get()) / 'settings.json'
        with open(path_to_setting, 'r') as f:
            data = json.load(f)
        logging.info(f'読み込んだsettings.json: {data}')
        
        SettingFrame.text_var_excel.set(data.get('text_var_excel', ''))
        SettingFrame.text_var_lib.set(data.get('text_var_lib', ''))
        SettingFrame.text_var_excel_ddl_filename.set(data.get('text_var_excel_ddl_filename', ''))
        SettingFrame.text_var_excel_dml_filename.set(data.get('text_var_excel_dml_filename', ''))
        SettingFrame.text_var_lib_filename.set(data.get('text_var_lib_filename', ''))
        SettingFrame.text_var_regex.set(data.get('text_var_regex', ''))
        SettingFrame.text_var_pkg_name.set(data.get('text_var_pkg_name', ''))
        SettingFrame.text_var_usr_name.set(data.get('text_var_usr_name', ''))
        SettingFrame.text_var_targetcode.set(data.get('text_var_targetcode', ''))
        SettingFrame.text_var_targetassets.set(data.get('text_var_targetassets', ''))
        SettingFrame.text_var_log.set(data.get('text_var_log', ''))
    
    def get_usrnames(self):
        logging.debug(f'list_lib: {Path(SettingFrame.text_var_lib.get()) / 'ddl'}')
        list_lib = (Path(SettingFrame.text_var_lib.get()) / 'ddl').glob('*.py')
        
        self.usrlist.delete(0, tk.END)
        for lib in list_lib:
            self.usrlist.insert(tk.END, lib.stem)
    
    def set_name(self, sw):
        name = self.usrlist.get(self.usrlist.curselection())
        if sw == 'pkg':
            logging.info(f'pkgを設定しました: {name}')
            SettingFrame.text_var_pkg_name.set(name)
        elif sw == 'usr':
            logging.info(f'usrを設定しました: {name}')
            SettingFrame.text_var_usr_name.set(name)
        
        

class LastFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(borderwidth=1,relief='groove')
        
        quit_btn = tk.Button(self, text='終了', command=self.quit).pack(pady=10)

app = Application()
app.mainloop()