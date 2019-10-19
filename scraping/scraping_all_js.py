import requests
import lxml
from bs4 import BeautifulSoup
from urllib import parse
import re
from scraping_all_url import all_url


js_box=[]
js_box_escape=[]

for path in all_url.urls:
    
    # # # 正規表現が現行のものでは漏れあり→漏れた分はtopスクレイピング時のif文で一時的にescapeに投げてる
    # link_directory_name= re.search(r'\w+', re.search(r'^/\w+/', path).group())
    # link_directory= f"link_box_{link_directory_name}"
    
    url= parse.urljoin('https://www.oshiire.co.jp/', path)
    html= requests.get(url)
    soup= BeautifulSoup(html.text, 'lxml')
    links= soup.findAll('script')
    
    for link in links:
        isJs= False
        if link.get('type') == 'text/javascript':
            isJs= True
        if not link.get('src') == None:
            isJs= True
        if isJs:
            js_box.append(link.get('src'))
        
    js_box= list(dict.fromkeys(js_box))
    js_box_escape= list(dict.fromkeys(js_box_escape))

# container.oshiireはまだescapeのまま
for links in js_box:  
    with open('all_js.py', 'a') as file:
        file.write("\n '%s'," % links)