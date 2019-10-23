import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
from urllib import parse
import os
import pathlib
import urllib.parse
from scraping_data.fromAll import allPageUrl
import re

# html版になってる


# 絶対パス用に変えた・・・つもり
def createDirectoryAndPutFiles(absolutePathes:list):
    for url in absolutePathes:
        
        # ディレクトリ・ファイル作成用data収集
        # (見本)/store//store_343
        pathStr= urllib.parse.urlparse(url).path
        
        # →/のみならindex.htmlに上書き
        # (見本)　/  =>  index.html
        if pathStr == '/':
            pathStr= '/index.html'
            
        # →末尾が/ならindex.htmlを付け加える
        # (見本)/store//store_343/  =>  /store//store_343/index.html
        if re.match('^.+/$', pathStr):
            pathStr= pathStr + 'index.html'
            
        # →末尾が何もないなら.htmlを付け加える
        # (見本)/store//store_343  =>  /store//store_343.html
        if not pathlib.Path(pathStr).suffix == '.html':
            pathStr= pathStr + '.html'
        # →//をなくす
        # (見本)/store//store_343/index.html  =>  /store/store_343/index.html
        if re.match('^.+(//).+$', pathStr):
            pathStr= pathStr.replace('//', '/')
        
        # ディレクトリ構造を文字列として保存
        # (見本)/store  =>  ./Result/store
        path= './Result'+os.path.dirname(pathStr)
        
        #./Resultの中の....pathStr！ってとこまで細かく
        # (見本)/store/store_343.html  =>  ./Result/store/store_343.html
        pathStr= './Result' + pathStr 
        
        
        # ./Result/←　こんな感じになっちゃうからね
        # /index.htmlの時はpathがこんな風になってるのでそれを条件に引っ掛けてる
        if pathStr == '/index.html':
            path= './Result'
        # htmlのtextデータ収集
        contents= requests.get(url).text
        
        # pathを与えるとそれ通りにディレクトリを作成する
        # ./Result/store => このディレクトリ内の、Resultディレクトリ内の、storeディレクトリを作るって感じ
        # 開発途中に際し、Fileがないぞ！エラーが起きた為、例外処理にて情報収集
        try:
            os.makedirs(path, exist_ok=True)
            with open(pathStr, 'w') as file:
                file.write(contents)
        except FileNotFoundError:
            print(path)
            print(pathStr)
            
# PDFとかimgとかhtmlじゃないものはエラーが出てるので明日対策

            
            
createDirectoryAndPutFiles(allPageUrl.urls)


# path
# ./Result//fc/pio
# ./Result//map
# /service/sifas/
# こういう形式にしたい

# →//をなくす
# →末尾が/ならindex.htmlを付け加える
# →末尾が何もないなら.htmlを付け加える
# 末尾が.htmlなら何もしない
# /store/store_343.html




