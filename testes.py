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
import datetime
import pathlib
from scraping_data.fromTop import topPageUrl


# 計測用スタート時間：関数外に配置
start= datetime.datetime.fromtimestamp(time.time())

link_boxG= []
link_boxG_escape=[]
link_box_formG=[]
logG= []



# linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
def reconstructionUrl(routeUrl:str, url:str, link:str):
    
    parse_link= urllib.parse.urlparse(link) 
    
    if not isValid(link):
        return False
    # 相対パスなら今来てるPathと繋げる
    if (parse_link.scheme)+(parse_link.netloc) == '':
        link= url+(parse_link.path)
    # 絶対パスならroutePathと繋げる
    if (parse_link.scheme)+(parse_link.netloc) == '' and re.match('^/', parse_link.path):
        link= routeUrl+(parse_link.path)
    # 以降はパーツがあるなら再構成していく
    if parse_link.params != '':  
        link= link+ ';'+ urllib.parse.quote(parse_link.params, encoding='utf-8')
    if parse_link.query != '':
        link= link+ '?'+ urllib.parse.quote(parse_link.query, encoding='utf-8')
    if parse_link.fragment != '':
        link= link+ '#'+urllib.parse.quote(parse_link.fragment, encoding='utf-8')
    
    return link


# 重複があれば削除, link切れを起こしてるものは削除
def checkDuplicateAndCheckAccess(urls:list):
    urls= list(dict.fromkeys(urls))
    for url in urls:
        try:
            forCheck= urllib.request.urlopen(url)
            forCheck.close()
        except urllib.error.URLError:
            urls.remove(url)
        except UnicodeEncodeError:
            print(url)
            print('error起きてます')
    return urls

# カスタム要素、エラーが起きそうなデータを弾くアルゴリズム
# return True or False
def isValid(link:str):
    tOrF= False
    if re.match('^tel:', link):
        return tOrF
    if re.match('^#', link):
        return tOrF
    tOrF= True
    return tOrF

# 指定のドメインなの？
def availableDomain(link_normarized:str):
    parse_link= urllib.parse.urlparse(link_normarized)
    tOrF= False
    # ----------------------------------ドメインがoshiireならlink_boxへ
    if (parse_link.netloc == 'www.oshiire.co.jp'): 
        tOrF= True
    # ------------------------ドメインがcontainer.oshiireならlink_boxへ
    if (parse_link.netloc == 'container.oshiire.co.jp'):
        tOrF= True
    return tOrF

# file保存（path, 保存file名, 材料になるlist）
def sDatasCorectToFileAsList(path:str, fileName:str, data:list):
    with open(f'{path}/{fileName}', 'a') as file:
        file.write("urls=[")
        for datum in data:  
            file.write("\n '%s'," % datum)
        file.write("\n]")

# file保存関数のセット、allurls仕様
def createDirectoryAndFile(link_boxes:list):
    # --------------------------------------------再帰が完全に終了後、重複があれば削除, link切れを起こしてるものも削除
    link_box= checkDuplicateAndCheckAccess(link_boxes[0])
    link_box_escape= checkDuplicateAndCheckAccess(link_boxes[1])
    link_box_form= checkDuplicateAndCheckAccess(link_boxes[2])
    
    # file保存（path, 保存file名, 材料になるlist）
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrl.py', link_box)  
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlEscape.py', link_box_escape) 
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlForm.py', link_box_form) 
        



# スープオブジェクト(aタグ, Fromタグ)生成
def createSoupObject(url:str):
    # html情報をget
    html= requests.get(url)
    # html.textを用いてBeautifulSoupのオブジェクト生成
    soupObject= BeautifulSoup(html.text, 'lxml')
    # BeautifulSoupのオブジェクトを用いて、html.textの内、aタグだけを収集
    linksATag= soupObject.findAll('a')
    # BeautifulSoupのオブジェクトを用いて、html.textの内、formタグだけを収集
    linksFormTag= soupObject.findAll('form')
    # aタグ、formタグの両方をreturnとして返したいので配列に詰める
    soupObject=[linksATag, linksFormTag]
    return soupObject

# スープオブジェクト(aタグ）内のurlを抽出、一定の形式に整形
def process_Atag(processingUrl:str, ATag):
    # aタグをurl化
    link= ATag.get('href')
    #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
    if link == None:
        return False
    #URLの再構成、そもそもURLがNoneの場合はFalseでcontinue 
    return reconstructionUrl('https://www.oshiire.co.jp', processingUrl, link)
        
        

    

# Formタグ用保存メソッド
def process_Formtag_and_add_to_lists(linksFormTag):
    for link in linksFormTag:
        # Formタグをurl化
        link= link.get('href')
        link_box_formG.append(link)




# 1つのURLから、そのURLに存在するurl達をかき集めて、再構成して、list化して返してくれる関数
def recursively_getting_urls_from_a_url(url:str):
    # 引数となったurlから取れるlink達の入れ物、
    link_box_Local=[]
    # recursionError対策
    sys.setrecursionlimit(10000) 
    # 処理済みURL（これから処理するURl）をlogに記録    
    logG.append(url)
    # ****************************************URLでgetリクエストを送り、htmlをget, aタグ, Formタグ抽出
    soupObject= createSoupObject(url)
    linksATag= soupObject[0]
    linksFormTag= soupObject[1]

    # ****************************************************************aタグの加工・仕分け・配列への保存
    for temp_link in linksATag:
        
        link_normarized= process_Atag(url, temp_link)
        if  not link_normarized:
            continue
        # -----------------------------------------------Domainがoshiire関係か？
        if availableDomain(link_normarized):
            link_boxG.append(link_normarized)
            link_box_Local.append(link_normarized)
            continue
        # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
        link_boxG_escape.append(link_normarized)
        
    # ******************************************************************************formタグの配列への保存
    process_Formtag_and_add_to_lists(linksFormTag)
    # ********************************************************************************再帰の箇所
    # 配列化したUrlを順番に取り出す→既に処理したことがあれば関数へ飛ばさずskip
    for link in link_box_Local:
        if link in logG:
            continue
        # jpgも紛れてくることがある
        if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.jpg':
            continue
        if (requests.get(link).status_code) >= 400:
            continue
        # 処理したことがなければ関数へ。
        recursively_getting_urls_from_a_url(link)
        
        # logG= list(dict.fromkeys(logG))
    
    
    return [link_boxG, link_boxG_escape, link_box_formG]









    

# # ******************************************************************************imageタグの仕分け
# for link in linksImageTag:
#     link= link.get('src')
#     linkAndparse_link= reconstructionUrl('https://www.oshiire.co.jp', url, link)
#     if linkAndparse_link == None:
#         continue
#     link_box_image.append(link)
# link_box_image= list(dict.fromkeys(link_box_image))

# file保存（path, 保存file名, 材料になるlist）
# sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlImg.py', link_box_image)  