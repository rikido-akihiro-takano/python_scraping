from scraping_data.fromTop import topPageUrl
import scrapingTools

  
# 全部のlinkを叩き出す用
link_boxes= scrapingTools.getAllFromALink(topPageUrl.urls)
# 叩き出したlinkをファイルに書き込む用
scrapingTools.createDirectoryAndFile(link_boxes)