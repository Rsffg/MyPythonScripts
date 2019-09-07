#! python3
# copyFile.py
"""
正規表現でファイル名決める際には，
https://regex101.com/
のサイトでヒットする文字をテストしてみること．
予想外なファイルもヒットする可能性があるので注意する．



"""
import os, re, shutil


### ここから①②③を設定する ###

# ①カレントディレクトリをsrcディレクトリに変更
homeDir = r'D:\Myfiles\WorkSpace\python\20190907_copyFiles\src'
os.chdir(homeDir)

# ②コピー先のフォルダパスを決める（★ここは間違えないように★）
copyDir = r'D:\Myfiles\WorkSpace\python\20190907_copyFiles\dst3'

# ③検索するファイル名をきめる（正規表現）
regex = re.compile(r'..T_.+')



###　ここから先は触らなくていい ###



# ディレクトリ走査
for curDir, subDirs, files in os.walk('.'):
    print('+curDir: ' + curDir)
    for subDir in subDirs:
        print(' +subDir: ' + subDir)
    for file in files:     
        #print('  +file: ' + file)
        mo = regex.search(file)
        if mo != None:
            # fileの格納先チェック（ない場合のみmkdir）
            dst = os.path.join(copyDir,curDir[2:])
            print('   >>dst: ' + dst)
            if not os.path.isdir(dst):
                os.makedirs(dst)
            src = os.path.join(curDir, file)
            print('   >>src: ' + src)
            shutil.copy(src, dst)
