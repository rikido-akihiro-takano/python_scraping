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
        
    parse_link= urllib.parse.urlparse(link)
    linkAndparse_link=[link, parse_link]
    return linkAndparse_link


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
def isValid(link:str):
    tOrF= False
    if re.match('^tel:', link):
        return tOrF
    if re.match('^#', link):
        return tOrF
    tOrF= True
    return tOrF

# 指定のドメインなの？
def availableDomain(link:str, parse_link:urllib.parse.ParseResult):
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
        




  
# 別のリンクをスクレイピングする際は要カスタマイズ
def getAllFromALink(link_box:list=[], link_box_escape:list=[], link_box_form:list=[], log:list=[]):
    sys.setrecursionlimit(10000) 
    # TopPageから取り出したURL群を順番に取り出してターゲットURLとして扱う

    
    for url in link_box:
        
        # --------------------------------------------------logData収集
        log.append(url)
        
        html= requests.get(url)
        soup= BeautifulSoup(html.text, 'lxml')
        
        #aタグ、formタグを全回収 
        linksATag= soup.findAll('a')
        linksFormTag= soup.findAll('form')
        # linksImageTag= soup.findAll('img')
        
        
        now = datetime.datetime.fromtimestamp(time.time())
        print('配列から1つのurl取り出し、html構造からurls取り出し、配列化したとこ')
        print(f'経過時間: {now.minute - start.minute}分{now.second - start.second}秒')
        
        # ターゲットURLに関連するURL達を収集する
        # ******************************************************************************aタグの仕分け
        for link in linksATag:
            # ----------------------------------------------------------------------------------URLの前処理
            link= link.get('href')
            
            #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
            if link == None:
                continue
            
            #URLの再構成、そもそもURLでない場合はNoneでcontinue 
            linkAndparse_link= reconstructionUrl('https://www.oshiire.co.jp', url, link)
            if linkAndparse_link == False:
                continue
            link= linkAndparse_link[0]
            parse_link= linkAndparse_link[1]
            
            # -----------------------------------------------Domainがoshiire関係か？
            if availableDomain(link, parse_link):
                link_box.append(link)
                continue
            # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
            link_box_escape.append(link)
            
            print('link_boxの長さ')
            print(len(link_box))
            print(len(link_box_escape))
            
        now = datetime.datetime.fromtimestamp(time.time())
        print('html構造から取り出したUrlsを再形成し終わったとこ')
        print(f'経過時間: {now.hour - start.hour}時間{now.minute - start.minute}分{now.second - start.second}秒')
        
        # ******************************************************************************formタグの仕分け
        for link in linksFormTag:
            link= link.get('href')
            link_box_form.append(link)
            
        # logに存在しているurlを抜いたlink_boxを再帰専用として作成、最終的に戻ってきた時に抜け分と結合でMax！
        # link_box_alt=  
        # link_box_escape= 
        # link_box_form=
        # skipされなければ再帰処理。現在のlink_box等のlistを飛ばす
        link_boxes= getAllFromALink(link_box, link_box_escape, link_box_form, log)
        # 再帰処理から帰ってきた各listの中身を呼び出し元へ反映
        link_box= link_box + link_boxes[0]
        link_box_escape= link_box_escape + link_boxes[1]
        link_box_form= link_box_form + link_boxes[2]
        log= log + link_boxes[3]
    
    # returnする用にlist化
    link_boxes=[link_box, link_box_escape, link_box_form, log]
    
    # return
    return link_boxes


# スープオブジェクト(Atag, Fromtag)生成
def createSoupObject(url:str, start):
    html= requests.get(url)
    now = datetime.datetime.fromtimestamp(time.time())
    print('html= requests.get(url)')
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    soupObject= BeautifulSoup(html.text, 'lxml')
    now = datetime.datetime.fromtimestamp(time.time())
    print("BeautifulSoup(html.text, 'lxml'")
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    linksATag= soupObject.findAll('a')
    now = datetime.datetime.fromtimestamp(time.time())
    print("linksATag= soupObject.findAll('a')")
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    linksFormTag= soupObject.findAll('form')
    now = datetime.datetime.fromtimestamp(time.time())
    print("linksFormTag= soupObject.findAll('form')")
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    soupObject=[linksATag, linksFormTag]
    now = datetime.datetime.fromtimestamp(time.time())
    print('oupObject=[linksATag, linksFormTag]')
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    return soupObject

# 第一引数: どのUrlのhtml内、aタグを処理中か？
# 第二引数: 処理予定のaタグ達
# 第三引数: 空のlist or 最終的なurl集約場所
# 第四引数: 第三引数の処理できなかったもの達
def process_Atag_and_add_to_lists(url:str, linksATag:list, link_box:list, link_box_escape:list, log:list):
    for link in linksATag:
        # aタグをurl化
        link= link.get('href')
        #Htmlから抜き出したaタグのhrefにはNoneもあって、typeErrorが起きるのでskip 
        if link == None:
            continue
        #URLの再構成、そもそもURLでない場合はFalseでcontinue 
        linkAndparse_link= reconstructionUrl('https://www.oshiire.co.jp', url, link)
        if linkAndparse_link == False:
            continue
        link= linkAndparse_link[0]
        parse_link= linkAndparse_link[1]
        
         # -----------------------------------------------Domainがoshiire関係か？
        if availableDomain(link, parse_link):
            link_box.append(link)
            continue
        # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
        link_box_escape.append(link)
    
    # return用に配列を二次元配列化
    link_boxes=[link_box, link_box_escape]
    return link_boxes

# Formタグ用保存メソッド
def process_Formtag_and_add_to_lists(linksFormTag, link_box_form):
    for link in linksFormTag:
        # Formタグをurl化
        link= link.get('href')
        link_box_form.append(link)
    return link_box_form
        
# 再帰部分をメソッド化
def process_of_recursive(link:str, log:str):

    # 再帰処理、returnはlink_boxes
    link_boxes= recursively_getting_urls_from_a_url(link)
    
    # 再帰処理後のlink_boxesとそれ以前のlink_boxesと結合させる
    link_box= link_boxes[0]
    link_box_escape= link_boxes[1]
    link_box_form= link_boxes[2]
    log= log + link_boxes[3]
    # logの重複削除
    log= list(dict.fromkeys(log))
    link_boxes=[link_box, link_box_escape, link_box_form, log]
    return link_boxes   


def support_of_recursive(link_boxes:list,link_box:list, link_box_escape:list, link_box_form:list, log:list):
    link_box= link_boxes[0] + link_box
    link_box_escape= link_boxes[1] + link_box_escape
    link_box_form= link_boxes[2] + link_box_form
    log= link_boxes[3]
    link_boxes=[link_box, link_box_escape, link_box_form, log]
    return link_boxes  




# 1つのURLから、そのURLに存在するurl達をかき集めて、再構成して、list化して返してくれる関数
def recursively_getting_urls_from_a_url(url:str,link_box:list=[], link_box_escape:list=[], link_box_form:list=[], log:list=[]):
    # recursionError対策
    sys.setrecursionlimit(10000) 
    
    # 処理済みURL（これから処理するURl）をlogに記録
    log.append(url)
    print(f'\n\n------------------------logの記録されたUrl数{len(log)}')
    with open('log.py', 'a') as file:
        file.write(f'\n{url}')
    print(f'------------------------今回処理のUrl: {url}')
    now_first = datetime.datetime.fromtimestamp(time.time())
    print('処理済みURL（これから処理するURl）をlogに記録')
    print(f'-------------------------------------------------------------経過時間: {now_first.minute - start.minute}分{now_first.second - start.second}秒\n')
    # ****************************************URLでgetリクエストを送り、htmlをget, aタグ, Formタグ抽出
    soupObject= createSoupObject(url, start)
    linksATag= soupObject[0]
    linksFormTag= soupObject[1]
    
    now = datetime.datetime.fromtimestamp(time.time())
    print('URLでgetリクエストを送り、htmlをget, aタグ, Formタグ抽出')
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    # ****************************************************************aタグの加工・仕分け・配列への保存
    processedATag= process_Atag_and_add_to_lists(url, linksATag, link_box, link_box_escape, log)
    link_box= processedATag[0]
    link_box_escape= processedATag[1]
    
    now = datetime.datetime.fromtimestamp(time.time())
    print('aタグの加工・仕分け・配列への保存')
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    # ******************************************************************************formタグの配列への保存
    processedFormTag= process_Formtag_and_add_to_lists(linksFormTag, link_box_form)
    link_box_form= processedFormTag

    now = datetime.datetime.fromtimestamp(time.time())
    print('formタグの配列への保存')
    print(f'-------------------------------------------------------------経過時間: {now.minute - start.minute}分{now.second - start.second}秒\n')
    print(f'-------------------------------------------------------------今回の総経過時間: {now.minute - now_first.minute}分{now.second - now_first.second}秒\n\n\n')
    # ********************************************************************************再帰の箇所
    # 配列化したUrlを順番に取り出す→既に処理したことがあれば関数へ飛ばさずskip
    for link in link_box:
        if link in log:
            continue
        # jpgも紛れてくることがある
        if (pathlib.Path(urllib.parse.urlparse(link).path).suffix) == '.jpg':
            continue
        if (requests.get(link).status_code) >= 400:
            continue
        # 処理したことがなければ関数へ。
        link_boxes= process_of_recursive(link, log)
        link_boxes= support_of_recursive(link_boxes, link_box, link_box_escape, link_box_form, log)
        link_box= link_boxes[0]
        link_box_escape= link_boxes[1]
        link_box_form= link_boxes[2]
        log= link_boxes[3]
                
    link_boxes=[link_box, link_box_escape, link_box_form, log]
    return link_boxes 









    

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