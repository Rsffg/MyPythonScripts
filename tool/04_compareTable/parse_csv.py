import csv, os, re, sys
from pathlib import Path

def get_schema(name):
    print(name)
    regex = re.compile(r'.+_(.+)\.csv')
    mo = regex.search(name)
    return mo.group(1)

def get_category(name):
    str = ''
    if 'ddl' in name:
        str = 'ddl'
    elif 'dml' in name:
        str = 'dml'
    return str

def modify_rows(rows):
    
    list = ('sys_created','sys_updated','a2')
    
    for delete_col in list:
        idx = 0
        try:
            # print(f'modify:{rows[0]}')
            idx = rows[0].index(delete_col)
        except:
            pass
        if idx > 0:
            print(f'{rows[0]}の{idx}を削除します')
            rows = [row[:idx] + row[idx+1:] for row in rows]
    
    return rows
     

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def make_csv(fp):
    with open(fp, newline='') as f:
        ddl = {}
        reader = csv.reader(f)
        category = get_category(fp.name)
        schema = get_schema(fp.name)
        
        for row in reader:
            name = row[0]
            data = row[1:]
            print(f'name: {name}, data:{data}')
            
            ddl.setdefault(name, []) #
            tmp_data = ddl[name]
            tmp_data.append(data)
        
        for key, rows in ddl.items():
            print(f'table: {key}, data: {rows}')
            fp2 = get_base_dir() / category / schema
            fp2.mkdir(parents=True, exist_ok=True)
            fp2 = fp2 / f'{key}.csv'
            
            #ddlの場合はheaderを作成
            if category == 'ddl':
                header = [k[0] for k in ddl[key]]
                headers.setdefault(schema, {})
                headers[schema].setdefault(key, header)
            
            #dmlの場合はheaderを取得してセット
            if category == 'dml':
                header = headers[schema][key]
                rows.insert(0, header)
                print(f'header: {header}')
                
                #不要なカラムを削除
                rows = modify_rows(rows)
            

            with open(fp2, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            
            
            
                
        
        
#main
headers = {}
os.chdir(get_base_dir())
list1 = get_base_dir().glob('ddl*.csv')
list2 = get_base_dir().glob('dml*.csv')

for fp in list1:
    make_csv(fp)

for fp in list2:
    make_csv(fp)

    