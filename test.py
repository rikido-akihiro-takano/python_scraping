import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
from urllib import parse
import os
import pathlib
from scraping_all_url import all_url

# /contact/contact_form/　こんな感じの相対パスを期待
def createDirectoryAndPutFiles(relativePath:list, routePath:str):
    # このディレクトリ内に展開したいので、ここ起点の相対パスに変更
    for url in urls:
        # ディレクトリ・ファイル作成用data収集
        path= './html/'+os.path.dirname(url)
        url= './html/'+url
        # ファイルの中身収集
        contents= requests.get(routePath + url).text
        # pathを与えるとそれ通りにディレクトリを作成する
        os.makedirs(path, exist_ok=True)
        with open(url, 'w') as file:
            file.write(contents)

urls=[
    '/category/store/area_hokkaido/prefecture_hokkaido',
    '/category/store/area_tohoku/prefecture_aomori',
    '/category/store/area_tohoku/prefecture_iwate',
    '/category/store/area_tohoku/prefecture_miyagi',
    ]

def urlConstructor(urls:list):
    for url in urls:
        if not(parse.urlparse(url).netloc) == 'www.oshiire.co.jp':
            path_seed= pathlib.Path(url) 
             
        if htto
            print(path_seed.relative_to('https://www.oshiire.co.jp'))


urlConstructor(all_url.urls)

# createDirectoryAndPutFiles(urls, 'https://www.oshiire.co.jp')



