from scraping_data.fromTop import topPageUrl
# import scrapingTools
import scrapingTools
import urllib.parse
import re
import unicodedata


  
# 全部のlinkを叩き出す用
# link_boxes= scrapingTools.getAllFromALink(topPageUrl.urls)
link_boxes= scrapingTools.recursively_getting_urls_from_a_url('https://www.oshiire.co.jp')
# 叩き出したlinkをファイルに書き込む用
scrapingTools.createDirectoryAndFile(link_boxes)



# ボツになったアルゴリズム
    # # --------------------------------------------------------------------------------------
    # # 複数のクエリ文字列がある場合はsplitで分割して各パート毎エンコードして、再び合体
    # if re.match("^.+\?.+$", parse_link.query):    
    #     # ?を区切りに分割、list化
    #     # 'service=文書保管?service=3D文書保管'　=> ['service=文書保管' , 'service=3D文書保管']
    #     quesries= re.split('\?', parse_link.query)
    #     # query初期化
    #     for part in quesries: 
    #         part= urllib.parse.quote(part, encoding='utf-8')
    #         query += f'?{part}'
    #     link= link+ query
    #     print(link)
    # --------------------------------------------------------------------------------------
    

# 詰まったエラー
# 'mailto://insoinfo＠kyoshin-soko.co.jp'
# ValueError: netloc 'www.insoinfo＠kyoshin-soko.co.jp' contains invalid characters under NFKC normalization
