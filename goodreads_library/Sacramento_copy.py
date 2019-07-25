#https://www.saclibrary.org/

#https://www.saclibrary.org/Search?searchtext=The+Berenstain+Bears+and+the+Blame+Game&searchmode=anyword

# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
url="https://www.saclibrary.org/Search?searchtext={}&searchmode=anyword"
colum=["cudosid","goodreadsid","title","author","goodreadsUrl","aclibraryUrl","detailUrl"]
file=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=file.add_sheet("Sacramento",cell_overwrite_ok=True)
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
        aclibraryUrl = url.format(re.sub('[^0-9a-zA-Z]+', '+', title+"+"+author))
        rs=requests.get(aclibraryUrl)
        soup = BeautifulSoup(rs.text, 'html.parser')
        link = soup.find("div", {"class": "SearchPreviewTitle"}).a["href"] if soup.find("div", {"class": "SearchPreviewTitle"}) else None
        searchTitle = soup.find("div", {"class": "SearchPreviewTitle"}).a.get_text() if soup.find("div", {"class": "SearchPreviewTitle"}) else None
        if searchTitle is title:
            link = soup.find("div", {"class": "SearchPreviewTitle"}).a["href"] if soup.find("div", {
                "class": "SearchPreviewTitle"}) else None
        else:
            link=None
        if link:
            detailUrl = "https://www.saclibrary.org" + link
        else:
            detailUrl = "None"

        sheet.write(j, 0, cudosid)
        sheet.write(j, 1, goodreadsid)
        sheet.write(j, 2, title)
        sheet.write(j,3,author)
        sheet.write(j, 4, goodreadsUrl)
        sheet.write(j, 5, aclibraryUrl)
        sheet.write(j, 6, detailUrl)
        file.save('Sacramento.xls')
        print(cudosid,goodreadsid,title,aclibraryUrl,detailUrl)