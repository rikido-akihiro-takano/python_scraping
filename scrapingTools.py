
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
import unicodedata


# 計測用スタート時間：関数外に配置
start= datetime.datetime.fromtimestamp(time.time())
# グローバル変数
# クエリ文字列以降はカット
link_boxG= []
# エラーが起きてたらくる
link_boxG_escape=[]
# クエリ文字列以降が繋がってるpass
link_boxG_optisons=[]
link_box_formG=[]
logG= []

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

# linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
def reconstructionUrl(routeUrl:str, url:str, link:str):
    parse_link= urllib.parse.urlparse(link) 
    
    # Noneだったりtelだったらその時点でFalseをreturnする
    if not isValid(link):
        return False
    print('\n\n\n------------------------------------------------------------スタート')
    print(f'今のurl: {url}')
    print(f'今のlink: {link}')
    print(parse_link.path)
    # urlの各パターンに対応
    # --------------------------------------------------------------------------------------
    # 絶対パスのみのパターン
    if (parse_link.scheme)+(parse_link.netloc) == '' and re.match('^/.+$', parse_link.path):
        link= routeUrl+(parse_link.path)
        link_only_top= routeUrl+(parse_link.path)
        print('------------------------------------------------------------絶対パス')
        print(link)
    # https://www.oshiire.co.jp ×　相対パスのパターン
    if url == routeUrl and not re.match('^/.+$', parse_link.path):
        link= url + '/' + (parse_link.path)
        link_only_top= url + '/' + (parse_link.path)
        print('------------------------------------------------------------絶対パスV2')
        print(link)
    # 〜〜〜〜〜〜〜〜〜〜〜〜.html ×　相対パスのパターン
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path) and (pathlib.Path(parse_link.path).suffix) == '.html' and not url == routeUrl:
        # /を区切り文字に、配列化
        url= re.split(r'/', url)
        url.pop(-1)
        url= '/'.join(url)
        link= url+ '/' +(parse_link.path)
        link_only_top= url+ '/' +(parse_link.path)
        print('------------------------------------------------------------相対パスV2')
        print(link)
    # 〜〜〜〜〜〜〜〜〜〜〜〜/〜〜/ × 相対パスのパターン　
    if (parse_link.scheme)+(parse_link.netloc) == ''  and not re.match('^/.+$', parse_link.path)and not (pathlib.Path(parse_link.path).suffix) == '.html' and not url == routeUrl:
        link= url+(parse_link.path)
        link_only_top= url+(parse_link.path)
        print('------------------------------------------------------------相対パス')
        print(link)
    # scheemaとnetcolが入ってるlinkはそれ用に再構成
    if (parse_link.scheme)+(parse_link.netloc) != '':
        link= (parse_link.scheme) + '://' + (parse_link.netloc) +(parse_link.path)
        link_only_top= (parse_link.scheme) + '://' + (parse_link.netloc) +(parse_link.path)
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
    links=[link, link_only_top]
    return links

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
    tOrF= True
    return tOrF

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
        return availableDomain(link_normarized)


# 画像系は取り敢えず保留
def suffixChecker(link:str):
    checker= True
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.jpg':
        checker= False
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.gif':
        checker= False
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.img':
        checker= False
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.png':
        checker= False
    if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.pdf':
        checker= False
    return checker
    
# Formタグ用保存メソッド
def process_Formtag_and_add_to_lists(linksFormTag):
    global link_box_formG
    for link in linksFormTag:
        # Formタグをurl化
        print(f'\n{link}')
        link_box_formG.append(f'\n{link}')
        link_box_formG= list(dict.fromkeys(link_box_formG))




# 1つのURLから、そのURLに存在するurl達をかき集めて、再構成して、list化して返してくれる関数
def recursively_getting_urls_from_a_url(url:str):
    
    global link_boxG
    global link_boxG_optisons
    global logG
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
        link_normarizeds= process_Atag(url, temp_link)
        # returnにはlist型のとき、bool型のときがある
        if not link_normarizeds:
            continue
        
        link_normarized= link_normarizeds[0]
        link_only_top= link_normarizeds[1]
        
        if not availableDomain(link_normarized):
            continue
        # pathが././系だったらskip
        if re.match("^(?=.*/\./\./).*$", urllib.parse.urlparse(link_normarized).path):
              continue
        # 画像系の拡張子でないかチェック
        if not suffixChecker(link_normarized):
              continue
        # 単一のurlなのにparamsやqueryが少し違うからといってurl一つ分に数えるのはあんまよくない！ということでぶった切る
        if urllib.parse.urlparse(link_normarized).params != '' or urllib.parse.urlparse(link_normarized).query != '' or urllib.parse.urlparse(link_normarized).fragment != '':
            # ぶった切る前のやつをoptisonsへ
            link_boxG_optisons.append(link_normarized)
            link_boxG_optisons= list(dict.fromkeys(link_boxG_optisons))
            # link_normarizedを上書き
            link_normarized= link_only_top
            print('****************************************変更後')
            print(link_normarized)
            print('*********************************************')
        # ここまででバリデーションはかけているのでストレートに入れる
        link_boxG.append(link_normarized)
        link_boxG= list(dict.fromkeys(link_boxG))
        # # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
        # link_boxG_escape.append(link_normarized)
        # link_boxG_escape= list(dict.fromkeys(link_boxG_escape))
        
    # ******************************************************************************formタグの配列への保存
    process_Formtag_and_add_to_lists(linksFormTag)
    # ********************************************************************************再帰の箇所
    # 配列化したUrlを順番に取り出す→既に処理したことがあれば関数へ飛ばさずskip
    num= 1
    print(f'\n\n\n\n頭||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
    print('(link情報)')
    print(f'-----------------------------------------------------------------------url:{url}')
    for link in link_boxG:
          print(f'{link}: {num}')
          num += 1
    print('--------------------------------------------------------------------------------------------------------------')       

    for link in link_boxG:
        # print(f'------------------------------------------------------------------now_link: {link}')
        if link in logG:
            continue
        # 処理したことがなければ関数へ。
        print(f'{link} と繋がりのあるURLを取ってくるよ')
        recursively_getting_urls_from_a_url(link)
        print(f'{link} は再帰閉じまーす')
        print(f'\n\n後||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        logG= list(dict.fromkeys(logG))
    
    return [link_boxG, link_box_formG, link_boxG_optisons]



# link_boxG系には毎回追加でUrlを加えていき、毎回重複を消す。再帰の為のデータベースであると同時にreturnの数値にもなる




# ------------------------------------------------------------------------------------------------------------
# 重複があれば削除, link切れを起こしてるものは削除
def checkDuplicateAndCheckAccess(urls:list):
    global link_boxG_escape
    urls= list(dict.fromkeys(urls))
    for url in urls:
        try:
            forCheck= urllib.request.urlopen(url)
            forCheck.close()
        except urllib.error.URLError:
            urls.remove(url)
        except UnicodeEncodeError:
            print(url)
            print('UnicodeEncodeError起きてます')
            link_boxG_escape.append(url)
            link_boxG_escape= list(dict.fromkeys(link_boxG_escape))
        except AttributeError:
            print(url)
            print('AttributeError起きてます')
            link_boxG_escape.append(url)
            link_boxG_escape= list(dict.fromkeys(link_boxG_escape))
    return urls


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
    # link_boxG_escapeをエラー起きたurl入れる専用に変更
    link_box= checkDuplicateAndCheckAccess(link_boxes[0])
    link_box_form= link_boxes[1]
    link_box_escape= link_boxG_escape
    link_box_optisons = link_boxes[2]
    
    # file保存（path, 保存file名, 材料になるlist）
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrl.py', link_box)  
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlEscape.py', link_box_escape) 
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlForm.py', link_box_form) 
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlOptisons.py', link_box_optisons) 
# ------------------------------------------------------------------------------------------------------------
