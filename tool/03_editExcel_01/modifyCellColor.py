#! python3
# modifyCellColor.py

"""
【内容】
指定したディレクトリ下にあるすべてのEXCELファイルについて，
指定した列にある指定したワードの色を変える．


"""
import os, re, shutil, openpyxl
from openpyxl.styles import Font


### ここから①②③を設定する ###

# ①変換したいエクセルがあるフォルダを指定する
homeDir = r'D:\Myfiles\WorkSpace\git\20190915_workcpace'
os.chdir(homeDir)

# ②変換後のエクセルファイルの格納先を指定する（別にしないと上書きされる）
copyDir = r'D:\Myfiles\WorkSpace\git\20190915_workcpace\編集後'

# ③検索する文字（複数指定可能）を指定する．
words = ['宛名番号','職員宛名番号']

# ④検索対象のフィル名・拡張子を指定する．
file_pattern = re.compile(r'.+\.xlsx')

# ⑤文字色を変える列を指定する
editColNum = 5


###　ここから先は触らなくていい ###
for filename in os.listdir('.'):
    mo = file_pattern.search(filename)

    if mo == None:
        continue

    print('openning file...'+ filename)

    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    for cell_obj in tuple(sheet.columns)[editColNum]:
        #print(cell_obj.value)
        if cell_obj.value in words:
            print('-->EXIST(' + cell_obj.value + ')')
            cell_obj.font = Font(color='FFC00000')
    wb.save(os.path.join(copyDir, filename))


