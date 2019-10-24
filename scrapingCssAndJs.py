import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import re
import urllib.parse
import urllib.request
import pdb
import sys
import time
import os
import datetime
import pathlib
import unicodedata
import scrapingTools
from scraping_data.fromAll import allPageUrl


# ローカル変数（list）定義
css_box=[]
js_box=[]

# ------------------------------------------------------reconstruction関係
def isValid(link:str):
    tOrF= False
    if link == './':
        return tOrF
    if link == '/':
        return tOrF
    if re.match('^tel:', link):
        return tOrF
    if re.match('^#', link):
        return tOrF
    if re.match('^#', link):
        return tOrF
    tOrF= True
    return tOrF

# スープオブジェクト(aタグ）内のurlを抽出、一定の形式に整形
def process_Atag(processingUrl:str, link):
    #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
    if link == None:
        return False
    #URLの再構成、そもそもURLがNoneの場合はFalseでcontinue 
    return reconstructionUrl('https://www.oshiire.co.jp', processingUrl, link)


# linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
def reconstructionUrl(routeUrl:str, url:str, link:str):
    parse_link= urllib.parse.urlparse(link) 
    
    # Noneだったりtelだったらその時点でFalseをreturnする
    if not isValid(link):
        return False
    
    # print('\n\n\n------------------------------------------------------------スタート')
    # print(f'今のurl: {url}')
    print(f'今のlink: {link}')
    print(parse_link.path)
    if parse_link.netloc != '' and parse_link.netloc != 'www.oshiire.co.jp':
        return False
    
    # urlの各パターンに対応
    # --------------------------------------------------------------------------------------
    # 絶対パスのみのパターン
    if (parse_link.scheme)+(parse_link.netloc) == '' and re.match('^/.+$', parse_link.path):
        link= routeUrl+(parse_link.path)
        print('------------------------------------------------------------絶対パス')
        print(link)
        
    # https://www.oshiire.co.jp ×　相対パスのパターン
    if url == routeUrl and not re.match('^/.+$', parse_link.path):
        link= url + '/' + (parse_link.path)
        print('------------------------------------------------------------絶対パスV2')
        print(link)
        
    # 〜〜〜〜〜〜〜〜〜〜〜〜.js ×　相対パスのパターン
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path) and (pathlib.Path(parse_link.path).suffix) == '.js' and not url == routeUrl:
        # /を区切り文字に、配列化
        url= re.split(r'/', url)
        url.pop(-1)
        url= '/'.join(url)
        link= url+ '/' +(parse_link.path)
        
        print('------------------------------------------------------------相対パスV-js')
        print(link)
    # 〜〜〜〜〜〜〜〜〜〜〜〜.css ×　相対パスのパターン
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path) and (pathlib.Path(parse_link.path).suffix) == '.css' and not url == routeUrl:
        # /を区切り文字に、配列化
        url= re.split(r'/', url)
        url.pop(-1)
        url= '/'.join(url)
        link= url+ '/' +(parse_link.path)
        print('------------------------------------------------------------相対パスV-css')
        print(link)
        
    # 〜〜〜〜〜〜〜〜〜〜〜〜/〜〜/ × 相対パスのパターン　
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path)and not url == routeUrl and not (pathlib.Path(parse_link.path).suffix) == '.css' and not (pathlib.Path(parse_link.path).suffix) == '.js':
        link= url+(parse_link.path)
        
        print('------------------------------------------------------------相対パス')
        print(link)
    # scheemaとnetcolが入ってるlinkはそれ用に再構成
    if (parse_link.scheme)+(parse_link.netloc) != '':
        link= (parse_link.scheme) + '://' + (parse_link.netloc) +(parse_link.path)
        
        print('------------------------------------------------------------フルパス')
        print(link)
    # --------------------------------------------------------------------------------------
    #クエリ文字列以下はcash bastingの為にブラウザ上でのみ必要なだけなので、ファイル名としてはいらない！
    
    if link == 'https://www.oshiire.co.jp/fc/pio/owner.htmlcss/reset.css':
        pdb.set_trace()
    
    return link

# -------------------------------------------------------------------



# ------------------------------------------------------タグ状態での検査
# cssファイルが潜むタグかどうかチェック
def forCssCheck(link:str):
    if link.get('rel')[0] == 'stylesheet':
        return True
    if link.get('type') == 'text/css':
        return True
    return False

# jsファイルが潜むタグかどうかチェック
def forJsCheck(link:str):
    if link.get('type') == 'text/javascript':
        return True
    if not link.get('src') == None:
        return True
    return False
# -------------------------------------------------------------------
            
#　ディレクトリ生成 
def createDirectoryAndPutFiles(absolutePathes:list):
    for url in absolutePathes:
        # ディレクトリ・ファイル作成用data収集
        # (見本)/store//store_343
        pathStr= urllib.parse.urlparse(url).path
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
        
        # 開発途中に際し、Fileがないぞ！エラーが起きた為、例外処理にて情報収集
        try:
            os.makedirs(path, exist_ok=True)
            # 第一引数のurl元からDL、第二引数のpathおよびファイル名で保存
            urllib.request.urlretrieve(url, pathStr)
        except urllib.error.HTTPError:
            print('エラーです') 
            print(url)
            print(pathStr)
            
# cssかjsか見分けて保存（最終チェック）
def Correct(link:str):
    global css_box
    global js_box
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.css':
        css_box.append(link)
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.js':
        js_box.append(link)


def getCssAndJs(urls:list):
    global css_box
    global js_box
 
    for url in urls:
        # その中のhtml情報から特定のタグを取ってくる
        cssLinks= BeautifulSoup(requests.get(url).text, 'lxml').findAll('link')
        jsLinks= BeautifulSoup(requests.get(url).text, 'lxml').findAll('script')
        
        print(f'\n\n\n\n\n-------------------------------------------------------------------------------------------------------------------------------処理中の{url}')
        # ----------------------------------------------------------------------------CSS
        # linkタグの中でも特定の条件下のものがcssファイルとして認識されるようにする
        # 認識済のcssはcss_boxへ保存
        for c_link in cssLinks:
            
            if not c_link:
                continue
            if not forCssCheck(c_link):
                continue
            # 整形後のc_link
            if not process_Atag(url, c_link.get('href')):
                continue
            # print('|||||||||||||||||||||||||||||||||||||||')
            # print('c_linkだよー')
            # print(process_Atag(url, c_link.get('href')))
            # print('|||||||||||||||||||||||||||||||||||||||')
            Correct(process_Atag(url, c_link.get('href')))
        
        # scriptタグの中でも特定の条件下のものがjsファイルとして認識されるようにする
        # 認識済のjsはjs_boxへ保存
        for j_link in jsLinks:
            
            if not j_link:
                continue
            if not forJsCheck(j_link):
                continue
            # 整形後のj_link
            if not process_Atag(url, j_link.get('src')):
                continue
            # ----------------------------------------------------------今j_linkにFalseが入ってる
            # print('|||||||||||||||||||||||||||||||||||||||')
            # print('j_linkだよー')
            # print(process_Atag(url, j_link.get('src')))
            # print('|||||||||||||||||||||||||||||||||||||||')
            Correct(process_Atag(url, j_link.get('src')))
        
        print('\n------------------------------------------------------------------------------------------------------------------------------------finish!!')
    # 全部終わったら重複削除
    css_box= list(dict.fromkeys(css_box))
    js_box= list(dict.fromkeys(js_box))    
    
    
    with open('testCss.py', 'a') as file:
        file.write("urls=[")
        for css in css_box:
            file.write("\n '%s'," % css)
        file.write("\n]")
        
    with open('testJs.py', 'a') as file:
        file.write("urls=[")
        for js in js_box:
            file.write("\n '%s'," % js)
        file.write("\n]")
    
    # # 一括DL and ディレクトリ作成・ファイル設置！
    # createDirectoryAndPutFiles(css_box)
    # createDirectoryAndPutFiles(js_box)
    
        
# getCssAndJs(allPageUrl.urls)

        
    
# -------------------------------------------------scrapingの対象url達を集める
# ローカル変数（list）定義
# link群取ってくる
# 個別に取り出す
# その中のhtml情報から特定のタグを取ってくる
# 内部構造があればその中のurlの部分を取ってくる
# 1つのurl内の全ての各タグを、各ローカル変数（list）に入れる

# -------------------------------------------------scrapingの対象url達を整形する
# どんなものがあるか見てみて、それに合うものを作る

# -------------------------------------------------scrapingの対象url達をディレクトリに配置する
# createDirectoryを参考に


# local.oshiiremove.rikido.net