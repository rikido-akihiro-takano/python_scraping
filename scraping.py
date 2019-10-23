import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.parse
import urllib.request

# ターゲットurl
# url= 'https://www.oshiire.co.jp'
url= 'https://www.oshiire.co.jp/store/store_298.html'

# ターゲットurlへGETリクエストのreturn
html= requests.get(url)

# BeautifulSoupで解析に使う種データ→BetifulSoupのインスタンスを生成
soup= BeautifulSoup(html.text, 'lxml')

# BetifulSoupのインスタンスからaタグのものだけ集約
links= soup.findAll('a')

# link_box_top(topページlink群)定義
link_box_top=[]
# topページlink群の内、絶対パスのモノ・パスでないモノ等、取り敢えず避けとく
link_box_top_escape=[]

# 繰り返し取り出し、aタグ内hrefを順次link_box_topに挿入、dict.fomkeys関数により重複分削除→list関数で再度配列化
for link in links:
    
    # ----------------------------------------------------------------URLの前処理
    
    # 未分解
    link= link.get('href')
    if link == None:
        continue
    print(link)
    # 分解済
    parse_link= urllib.parse.urlparse(link)
    
    #URlを各パーツに分解し、値があれば順次合体させていく
    if (parse_link.scheme) or (parse_link.netloc) == '':
        link= url+(parse_link.path)
    if parse_link.params != '':  
        link= link+ ';'+ (parse_link.params)
    if parse_link.query != '':
        link= link+ '?'+ urllib.parse.quote(parse_link.query, encoding='utf-8')
    if parse_link.fragment != '':
        link= link+ '#'+urllib.parse.quote(parse_link.fragment, encoding='utf-8')
    parse_link= urllib.parse.urlparse(link)

    # --------------------------------------------link切れを起こしていないものだけ通過
    try:
        forCheck= urllib.request.urlopen(link)
        forCheck.close()
    except urllib.error.URLError:
        continue
    # -----------------------------------------------------------------最後の仕分け
    # ドメインがoshiireならlink_boxへ
    if (parse_link.netloc == 'www.oshiire.co.jp'): 
        link_box_top.append(link)
        continue
    # ドメインがcontainer.oshiireならlink_boxへ
    if (parse_link.netloc == 'container.oshiire.co.jp'):
        link_box_top.append(link)
        continue
    # 上記に当てはまらないならlink_box_top_escapeへ
    link_box_top_escape.append(link)


# 重複したurlを削除・hash型（？）になってしまうので再度配列化
# →shunou-blogが漏れてるけど、そもそもアクセスできない→escapeに落ちてる
link_box_top= list(dict.fromkeys(link_box_top))
link_box_top_escape= list(dict.fromkeys(link_box_top_escape))

# ファイルをopen,「url=[」、「linksの中身（繰り返し）」、「\n]]、close（この記法ならclose省略可）という流れ
with open('testUrl.py', 'a') as file:
    file.write("urls=[")
    for link in link_box_top:  
        file.write("\n '%s'," % link)
    file.write("\n]")

with open('testUrlEscape.py', 'a') as file:
    file.write("urls=[")
    for link in link_box_top_escape:  
        file.write("\n '%s'," % link)
    file.write("\n]")
    
    
    
        

