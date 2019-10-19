import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import re
import urllib.parse
import urllib.request
import pdb
from scraping_data.fromTop import topPageUrl


def reconstructionUrl(routeUrl:str, url:str, link:str):
    
    # linkをパーツ毎にバラバラに。パーツ毎のチェックを行いつつ再構成していく
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


# --------------------------------------------重複があれば削除, link切れを起こしてるものは削除
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

# file保存（path, 保存file名, 材料になるlist）
def sDatasCorectToFileAsList(path:str, fileName:str, data:list):
    with open(f'{path}/{fileName}', 'a') as file:
        file.write("urls=[")
        for datum in data:  
            file.write("\n '%s'," % datum)
        file.write("\n]")

def isValid(parse_link:urllib.parse.ParseResult):
    if re.match('^tel:', parse_link.path):
        return False
    if re.match('^#', parse_link.path):
        return False
    return True

def availableDomain(link:str, parse_link:urllib.parse.ParseResult):
    tOrF= False
    # ----------------------------------ドメインがoshiireならlink_boxへ
    if (parse_link.netloc == 'www.oshiire.co.jp'): 
        tOrF= True
    # ------------------------ドメインがcontainer.oshiireならlink_boxへ
    if (parse_link.netloc == 'container.oshiire.co.jp'):
        tOrF= True
    return tOrF
    
    
# 別のリンクをスクレイピングする際は要カスタマイズ
def getAllFromALink(link_box:list, link_box_escape:list, link_box_form:list, log:list):
    # link_box_image=[]

    for url in topPageUrl.urls:
        
        html= requests.get(url)
        soup= BeautifulSoup(html.text, 'lxml')
        
        #aタグ、formタグを全回収 
        linksATag= soup.findAll('a')
        linksFormTag= soup.findAll('form')
        # linksImageTag= soup.findAll('img')
        
        # ******************************************************************************aタグの仕分け
        for link in linksATag:
        # ----------------------------------------------------------------------------------URLの前処理
            link= link.get('href')
            #URLの再構成、そもそもURLでない場合はNoneでcontinue 
            linkAndparse_link= scrapingTools.reconstructionUrl('https://www.oshiire.co.jp', url, link)
            if linkAndparse_link == None:
                continue
            link= linkAndparse_link[0]
            parse_link= linkAndparse_link[1]
            
            # -----------------------------------------------Domainがoshiire関係か？
            if scrapingTools.availableDomain(link, parse_link):
                link_box.append(link)
                continue
            # --------------------------Domainがoshiire関係でないならlink_box_escapeへ
            link_box_escape.append(link)

        # ******************************************************************************formタグの仕分け
        for link in linksFormTag:
            link= link.get('href')
            link_box_form.append(link)
        
        # # ******************************************************************************imageタグの仕分け
        # for link in linksImageTag:
        #     link= link.get('src')
        #     linkAndparse_link= scrapingTools.reconstructionUrl('https://www.oshiire.co.jp', url, link)
        #     if linkAndparse_link == None:
        #         continue
        #     link_box_image.append(link)
        # link_box_image= list(dict.fromkeys(link_box_image))

    # --------------------------------------------重複があれば削除, link切れを起こしてるものも削除
    link_box= scrapingTools.checkDuplicateAndCheckAccess(link_box)
    link_box_escape= scrapingTools.checkDuplicateAndCheckAccess(link_box_escape)
    link_box_escape= scrapingTools.checkDuplicateAndCheckAccess(link_box_form)

    # file保存（path, 保存file名, 材料になるlist）
    scrapingTools.sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrl.py', link_box)  
    scrapingTools.sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlEscape.py', link_box_escape) 
    scrapingTools.sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlForm.py', link_box_form) 
    # scrapingTools.sDatasCorectToFileAsList('./scraping_data/fromAll', 'allPageUrlImg.py', link_box_image)  
     
    