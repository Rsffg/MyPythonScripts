#! python3
# copyFile.py

import os, re, shutil


# カレントディレクトリをsrcディレクトリに変更
homeDir = r'D:\Myfiles\WorkSpace\python\2019-3-9\src'
os.chdir(homeDir)

# コピー先のフォルダパスを決める
copyDir = r'D:\Myfiles\WorkSpace\python\2019-3-9\dst'

# 検索するファイル名をきめる（正規表現）
regex = re.compile(r'.*EA_CHOSA*')

# コピー先のフォルダ名を決める（正規表現）
regex2 = re.compile(r'.*\\(\d+_.*?)(\\|$)')

# ディレクトリ走査
for curDir, subDirs, files in os.walk('.'):
    print('+curDir: ' + curDir)
    for subDir in subDirs:
        print(' +subDir: ' + subDir)
    for file in files:     
        print('  +file: ' + file)
        mo = regex.search(file)
        if mo != None:
            mo2 = regex2.search(curDir)
            if mo2 == None:
                print('   cant get name of copy dir')
                continue # コピー先のフォルダ名が取得できないとコピーしない
            print('    mo2: ' + mo2.group(1))
            dst = os.path.join(copyDir, mo2.group(1))
            print('    dst: ' + dst)
            if not os.path.isdir(dst):
                os.makedirs(dst) # コピー先にフォルダがなければ作る
            src = os.path.join(curDir, file)
            print('    src: ' + src)
            shutil.copy(src, dst)
            

# ファイル名に一致するものをコピーする
