# https://library.cityofpaloalto.org/
# https://paloalto.bibliocommons.com/v2/search?query=Beastly%20Babies&searchType=smart
# https://paloalto.bibliocommons.com/item/show/1270333136

# https://paloalto.bibliocommons.com/v2/search?custom_edit=false&query=title%3A%28Goldilocks+and+the+Three+Bears%29+++-contributor%3A%28Sarah+Delmege%29&searchType=bl&suppress=true
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
url="https://paloalto.bibliocommons.com/v2/search?query={}&searchType=smart"
colum=["cudosid","goodreadsid","title","author","goodreadsUrl","aclibraryUrl","detailUrl"]
file=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=file.add_sheet("Pali_Alto",cell_overwrite_ok=True)
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
        link = soup.find("h2", {"class": "cp-title"}).a["href"] if soup.find("h2", {"class": "cp-title"}) else None

        if link:
            detailUrl = "https://paloalto.bibliocommons.com" + link
        else:
            detailUrl = "None"

        sheet.write(j, 0, cudosid)
        sheet.write(j, 1, goodreadsid)
        sheet.write(j, 2, title)
        sheet.write(j,3,author)
        sheet.write(j, 4, goodreadsUrl)
        sheet.write(j, 5, aclibraryUrl)
        sheet.write(j, 6, detailUrl)
        file.save('Pali_Alto.xls')
        print(cudosid,goodreadsid,title,aclibraryUrl,detailUrl)