import requests
import lxml
from bs4 import BeautifulSoup
from urllib import parse
import re
from scraping_all_url import all_url


css_box=[]
css_box_escape=[]

for path in all_url.urls:
    
    # # # 正規表現が現行のものでは漏れあり→漏れた分はtopスクレイピング時のif文で一時的にescapeに投げてる
    # link_directory_name= re.search(r'\w+', re.search(r'^/\w+/', path).group())
    # link_directory= f"link_box_{link_directory_name}"
    
    url= parse.urljoin('https://www.oshiire.co.jp/', path)
    html= requests.get(url)
    soup= BeautifulSoup(html.text, 'lxml')
    links= soup.findAll('link')
    
    for link in links:
        isCss= False
        if link.get('rel')[0] == 'stylesheet':
            isCss= True
        if link.get('type') == 'text/css':
            isCss= True
            
        if isCss:
            css_box.append(link.get('href'))
        
    css_box= list(dict.fromkeys(css_box))
    css_box_escape= list(dict.fromkeys(css_box_escape))

# container.oshiireはまだescapeのまま
for links in css_box:  
    with open('all_css_link.py', 'a') as file:
        file.write("\n '%s'," % links)