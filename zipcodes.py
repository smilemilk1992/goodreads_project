# -*- coding: utf-8 -*-
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

rs=requests.get("https://www.nowmsg.com/us/all_state.asp")
soup = BeautifulSoup(rs.text,"html.parser")
print soup