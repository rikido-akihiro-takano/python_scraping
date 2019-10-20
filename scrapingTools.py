import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import re
import urllib.parse
import urllib.request
import pdb
from scraping_data.fromTop import topPageUrl



# linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
def reconstructionUrl(routeUrl:str, url:str, link:str):
    
    parse_link= urllib.parse.urlparse(link) 
    
    if not isValid(parse_link):
        return None
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
def isValid(parse_link:urllib.parse.ParseResult):
    if re.match('^tel:', parse_link.path):
        return False
    if re.match('^#', parse_link.path):
        return False
    return True

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
    # file保存（path, 保存file名, 材料になるlist）
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrl.py', link_boxes[0])  
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlEscape.py', link_boxes[1]) 
    sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlForm.py', link_boxes[2]) 
        
    
    
    
# 別のリンクをスクレイピングする際は要カスタマイズ
def getAllFromALink(link_box:list=[], link_box_escape:list=[], link_box_form:list=[], log:list=[], timesLog:int= 0):

    # TopPageから取り出したURL群を順番に取り出してターゲットURLとして扱う
    for url in link_box:
        
        # 再帰処理関係
        #--------------------------------------------------logと比較。既にスクレイピング済のURLならskip 
        if url in log:
            continue
        # 基本的に最後の最後でlist_box達を重複削除しようと思うが、増えすぎてエラーが出るかも、、、
        # ということで関数が300回転したら重複削除
        if timesLog == 300:
            link_box= list(dict.fromkeys(link_box))
            link_box_escape= list(dict.fromkeys(link_box_escape))
            link_box_form= list(dict.fromkeys(link_box_form))
            timesLog= 0
            
        # -------------------------------------------------timesLog追加
        timesLog += 1
        # --------------------------------------------------logData収集
        log.append(url)
        
        
        html= requests.get(url)
        soup= BeautifulSoup(html.text, 'lxml')
        
        #aタグ、formタグを全回収 
        linksATag= soup.findAll('a')
        linksFormTag= soup.findAll('form')
        # linksImageTag= soup.findAll('img')
        
        # ターゲットURLに関連するURL達を収集する
        # ******************************************************************************aタグの仕分け
        for link in linksATag:
        # ----------------------------------------------------------------------------------URLの前処理
            link= link.get('href')
            
            #URLの再構成、そもそもURLでない場合はNoneでcontinue 
            linkAndparse_link= reconstructionUrl('https://www.oshiire.co.jp', url, link)
            if linkAndparse_link == None:
                continue
            link= linkAndparse_link[0]
            parse_link= linkAndparse_link[1]
            
            # -----------------------------------------------Domainがoshiire関係か？
            if availableDomain(link, parse_link):
                link_box.append(link)
                continue
            # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
            link_box_escape.append(link)

        # ******************************************************************************formタグの仕分け
        for link in linksFormTag:
            link= link.get('href')
            link_box_form.append(link)
            

        # skipされなければ再帰処理。現在のlink_box等のlistを飛ばす
        link_boxes= getAllFromALink(link_box, link_box_escape, link_box_form, log, timesLog)
        # 再帰処理から帰ってきた各listの中身を呼び出し元へ反映
        link_box= link_boxes[0]
        link_box_escape= link_boxes[1]
        link_box_form= link_boxes[2]
        log= link_boxes[3]
        timesLog= link_boxes[4]
        

    # --------------------------------------------再帰が完全に終了後、重複があれば削除, link切れを起こしてるものも削除
    link_box= checkDuplicateAndCheckAccess(link_box)
    link_box_escape= checkDuplicateAndCheckAccess(link_box_escape)
    link_box_escape= checkDuplicateAndCheckAccess(link_box_form)
    
    # returnする用にlist化
    link_boxes=[link_box, link_box_escape, link_box_form, log, timesLog]
    
    # return
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