import requests
import lxml
from bs4 import BeautifulSoup
from urllib import parse
import re
from scraping_data.fromAll import allPageUrl


# ローカル変数（list）定義
css_box=[]
css_box_escape=[]

# link群取ってくる
for url in allPageUrl.urls:
# 個別に取り出す

    # その中のhtml情報から特定のタグを取ってくる
    html= requests.get(url)
    soup= BeautifulSoup(html.text, 'lxml')
    links= soup.findAll('link')
    
    # linkタグの中でも特定の条件下のものがcssファイルとして認識されるようにする
    for link in links:
        isCss= False
        if link.get('rel')[0] == 'stylesheet':
            isCss= True
        if link.get('type') == 'text/css':
            isCss= True
        # 特定の条件下のもの= Trueのものの、urlの部分を取ってくる
        # そしてそれを# ローカル変数（list）にいれる
        if isCss:
            css_box.append(link.get('href'))
            
            
# *************************************************************再形成関係未完
    
    
    # 全部終わったら重複削除
    css_box= list(dict.fromkeys(css_box))
    css_box_escape= list(dict.fromkeys(css_box_escape))

# cssのurlを収集
for links in css_box:  
    with open('all_css_link.py', 'a') as file:
        file.write("\n '%s'," % links)
        
    
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