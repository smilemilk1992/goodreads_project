# -*- coding: utf-8 -*-
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)

class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

s = requests.Session()
s.mount('https://www.nowmsg.com/', DESAdapter())
r = s.get("https://www.nowmsg.com/us/all_state.asp")
r.encoding = 'utf8'
soup = BeautifulSoup(r.text,"html.parser")
divs = soup.find_all("div",{"class":"col-sm-3"})
with open("douban.txt","w") as f:
    for div in divs:
        url = "https://www.nowmsg.com/us/"+div.find("a")["href"]
        # name = div.find("a").get_text().replace(" (AL)","").strip()  #州
        name=re.search("(.*?)\((.*?)\)",div.find("a").get_text()).group(1).strip()
        ss = re.search("(.*?).*?\((.*?)\)",div.find("a").get_text()).group(2).strip()
        # ss=div.find("a").get_text().rstrip(")").split(" (")
        # name=ss[0]
        # n=ss[1]
        r1 = s.get(url)
        r1.encoding = 'utf8'
        soup1 = BeautifulSoup(r1.text,"lxml")
        ass = soup1.find_all("div",class_="well")[1].find_all("a")
        for a in ass:
            url1 = "https://www.nowmsg.com/us/{}/".format(name)+a["href"]
            name1=a.get_text()  #城市
            r2 = s.get(url1)
            r2.encoding = 'utf8'
            soup2 = BeautifulSoup(r2.text, "lxml")
            ass = soup2.find_all("div", class_="well")[1].find_all("a")[0].get_text()
            print name,ss,name1,ass
            f.write(name+"\t"+ss+"\t"+name1+"\t"+ass+"\n")

