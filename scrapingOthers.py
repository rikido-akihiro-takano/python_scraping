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
from scraping_data.fromTop import topPageUrl
import unicodedata
from scraping_data.fromAll import allPageUrl


# ローカル変数（list）定義
jpg_box=[]
pdf_box=[]
img_box=[]
gif_box=[]
png_box=[]

# 保存
def Correct(link:str):
    global jpg_box
    global pdf_box
    global img_box
    global gif_box
    global png_box
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.jpg':
        jpg_box.append(link)
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.pdf':
        pdf_box.append(link)
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.img':
        img_box.append(link)
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.gif':
        gif_box.append(link)
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.png':
        png_box.append(link)

# 拡張子チェッカー
def suffixChecker(link:str):
    tOrF= False
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.jpg':
        tOrF= True
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.pdf':
        tOrF= True
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.img':
        tOrF= True
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.gif':
        tOrF= True
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.png':
        tOrF= True
    return tOrF
        
# カスタム要素、エラーが起きそうなデータを弾くアルゴリズム
# return True or False
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
def process_Atag(processingUrl:str, link:str):
    # aタグをurl化
    temp_link= link.get('href')
    #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
    if temp_link == None:
        return False
    #URLの再構成、そもそもURLがNoneの場合はFalseでcontinue 
    return reconstructionUrl('https://www.oshiire.co.jp', processingUrl, temp_link)


# linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
def reconstructionUrl(routeUrl:str, url:str, link:str):
    parse_link= urllib.parse.urlparse(link) 
    
    # Noneだったりtelだったらその時点でFalseをreturnする
    if not isValid(link):
        return False
    if not suffixChecker(link):
        return False
    print('\n\n\n------------------------------------------------------------スタート')
    print(f'今のurl: {url}')
    print(f'今のlink: {link}')
    print(parse_link)
    # urlの各パターンに対応
    parse_path= urllib.parse.quote(parse_link.path, encoding='utf-8')
    
    # --------------------------------------------------------------------------------------
    # 絶対パスのみのパターン
    if (parse_link.scheme)+(parse_link.netloc) == '' and re.match('^/.+$', parse_link.path):
        link= routeUrl+(parse_path)
        print('------------------------------------------------------------絶対パス')
        print(link)
    # https://www.oshiire.co.jp ×　相対パスのパターン
    if url == routeUrl and not re.match('^/.+$', parse_link.path):
        link= url + '/' + (parse_path)
        print('------------------------------------------------------------絶対パスV2')
        print(link)
    # 〜〜〜〜〜〜〜〜〜〜〜〜.html ×　相対パスのパターン
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path) and (pathlib.Path(parse_link.path).suffix) == '.html' and not url == routeUrl:
        # /を区切り文字に、配列化
        url= re.split(r'/', url)
        url.pop(-1)
        url= '/'.join(url)
        link= url+ '/' +(parse_path)
        print('------------------------------------------------------------相対パスV2')
        print(link)
    # 〜〜〜〜〜〜〜〜〜〜〜〜/〜〜/ × 相対パスのパターン　
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path)and not (pathlib.Path(parse_link.path).suffix) == '.html' and not url == routeUrl:
        link= url+(parse_path)
        print('------------------------------------------------------------相対パス')
        print(link)
    # scheemaとnetcolが入ってるlinkはそれ用に再構成
    if (parse_link.scheme)+(parse_link.netloc) != '':
        link= (parse_link.scheme) + '://' + (parse_link.netloc) +(parse_path)
        print('------------------------------------------------------------フルパス')
        print(link)
    # --------------------------------------------------------------------------------------
    
    
    # 以降はパーツがあるなら再構成していく
    # --------------------------------------------------------------------------------------
    # params
    if parse_link.params != '':  
        link= link+ ';'+ urllib.parse.quote(parse_link.params, encoding='utf-8')
        print('------------------------------------------------------------params')
        print(link)
    # query
    if parse_link.query != '':
        link= link+ '?'+ (urllib.parse.quote(parse_link.query, encoding='utf-8'))
        print('------------------------------------------------------------query')
        print(link)
    # fragment
    if parse_link.fragment != '':
        link= link+ '#'+urllib.parse.quote(parse_link.fragment, encoding='utf-8')
        print('------------------------------------------------------------fragment')
        print(link)
    # --------------------------------------------------------------------------------------
    
    return link

# 指定のドメインなの？
def availableDomain(link_normarized:str):
    
    try:
        parse_link= urllib.parse.urlparse(link_normarized)
        tOrF= False
        # ----------------------------------ドメインがoshiireならlink_boxへ
        if (parse_link.netloc == 'www.oshiire.co.jp'): 
            tOrF= True
        # ------------------------ドメインがcontainer.oshiireならlink_boxへ
        if (parse_link.netloc == 'container.oshiire.co.jp'):
            tOrF= True
        return tOrF
    # 文字コードの正規化に失敗したよ！みたいなエラーが出たので、手動で正規化してます
    except ValueError:
        link_normarized= unicodedata.normalize("NFKC", link_normarized)
        availableDomain(link_normarized)
        
# pdf用
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
        except UnicodeEncodeError:
            print('エラーです') 
            print(url)
            print(pathStr)
            
# エンコードしないとpdfを読み込んでくれなくて、すればファイル名が文字化けみたいになっちゃう〜ということで
# どうしようか考え中


def scrapingOthers(urls):
    global jpg_box
    global pdf_box
    global img_box
    global gif_box
    global png_box
    # link群取ってくる
    for url in urls:
        # BeautifulSoupオブジェクトs(aタグ達)
        links= BeautifulSoup(requests.get(url).text, 'lxml').findAll('a')
        for link in links:
            #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
            if link == None:
                continue
            # スープオブジェクト(aタグ）内のurlを抽出、一定の形式に整形
            link= process_Atag(url, link)
            if not availableDomain(link):
                continue
            # pathから拡張子が.pdf .img .gif .pngのいづれかであることをチェック！一致してたら格納！
            Correct(link)

    # 全部終わったら重複削除
    jpg_box= list(dict.fromkeys(jpg_box))
    pdf_box= list(dict.fromkeys(pdf_box))
    img_box= list(dict.fromkeys(img_box))
    gif_box= list(dict.fromkeys(gif_box))
    png_box= list(dict.fromkeys(png_box))

    # 一括DL and ディレクトリ作成・ファイル設置！
    createDirectoryAndPutFiles(jpg_box)
    createDirectoryAndPutFiles(pdf_box)
    createDirectoryAndPutFiles(img_box)
    createDirectoryAndPutFiles(gif_box)
    createDirectoryAndPutFiles(png_box)




scrapingOthers(allPageUrl.urls)

    # 各拡張子ごとの処理方法を調べて追記
    
    # # cssのurlを収集
    # for links in css_box:  
    #     with open('all_css_link.py', 'a') as file:
    #         file.write("\n '%s'," % links)


# .pdf
# .img
# .gif
# .png


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

