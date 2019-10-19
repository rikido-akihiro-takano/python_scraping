import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.parse
import urllib.request
from scraping_data.fromTop import topPageUrl
import scrapingTools
import pdb

  
        

link_box=[]   
link_box_escape=[]   
link_box_form=[]
log=[]
  
getAllFromALink(link_box, link_box_escape, link_box_form, log)