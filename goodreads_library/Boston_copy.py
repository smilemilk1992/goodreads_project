# -*- coding: utf-8 -*-
#https://www.bpl.org/
#https://bpl.bibliocommons.com/v2/search?query=Dr.%20Seuss%27s%20ABC&searchType=smart

import re
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
url="https://bpl.bibliocommons.com/v2/search?query={}&searchType=smart"
colum=["cudosid","goodreadsid","title","author","goodreadsUrl","aclibraryUrl","detailUrl"]
file=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=file.add_sheet("Boston_copy",cell_overwrite_ok=True)
for i in colum:
    sheet.write(0, colum.index(i), i)
j=0
with open('cudos_goodreads.txt', "r") as f:
    datas = f.readlines()
    for data in datas:
        j = j + 1
        data=data.strip().split("\t")
        cudosid=int(data[0])
        goodreadsid=int(data[1].replace("https://www.goodreads.com/book/show/",""))
        goodreadsUrl=data[1]
        title=data[2]
        author=data[3]
        # 去掉标题 ？：！()后面的内容
        title = re.split("\?|:|!|\(", title)[0]
        # 去掉标题里面英文标签以及括号
        title = re.sub(",|!|\?|:|;|\|-|\[|\]|\(|\)", '', re.split("\?|:|!", title)[0])
        # 去掉Jr.后缀,并且取第一个作者做搜索关键字
        author = author.split(",")[0].replace("Jr.", "")
        aclibraryUrl = url.format(re.sub('[^0-9a-zA-Z]+', '%20', title+" "+author))
        rs=requests.get(aclibraryUrl)
        soup = BeautifulSoup(rs.text, 'html.parser')
        link = soup.find("h2", {"class": "cp-title"}).a["href"] if soup.find("h2", {"class": "cp-title"}) else None
        if link:
            detailUrl = "https://bpl.bibliocommons.com" + link
            _title = soup.find("h2", {"class": "cp-title"}).find("span",{"class": "title-content"}).get_text().strip().replace("\n", "")
            if data[2].lower() not in _title.lower():  # 比对标题
                detailUrl = "None"
        else:
            detailUrl = "None"

        sheet.write(j, 0, cudosid)
        sheet.write(j, 1, goodreadsid)
        sheet.write(j, 2, title)
        sheet.write(j,3,author)
        sheet.write(j, 4, goodreadsUrl)
        sheet.write(j, 5, aclibraryUrl)
        sheet.write(j, 6, detailUrl)
        file.save('Boston_copy.xls')
        print(cudosid,goodreadsid,title,aclibraryUrl,detailUrl)