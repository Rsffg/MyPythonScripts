import csv, os, re
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
            fp2 = Path(__file__).parent / category / schema
            fp2.mkdir(parents=True, exist_ok=True)
            fp2 = fp2 / f'{key}.csv'
            
            with open(fp2, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        
#main
os.chdir(Path(__file__).parent)
list = Path(__file__).parent.glob('*.csv')

for fp in list:
    make_csv(fp)

    
    