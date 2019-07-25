# https://www.nypl.org/
# https://browse.nypl.org/iii/encore/search/C__SBeastly%20Babies__Orightresult__U?searched_from=header_search&timestamp=1563462043347&lang=eng
# https://browse.nypl.org/iii/encore/record/C__Rb20641029__SBeastly%20Babies__Orightresult__U__X7;jsessionid=1BE499247543732742E953648D3B2784?lang=eng&suite=def
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
url="https://browse.nypl.org/iii/encore/search/C__S{}__Orightresult__U?searched_from=header_search&lang=eng"
colum=["cudosid","goodreadsid","title","author","goodreadsUrl","aclibraryUrl","detailUrl"]
file=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=file.add_sheet("New_York",cell_overwrite_ok=True)
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
        if "None" in author:
            aclibraryUrl =url.format(re.sub('[^0-9a-zA-Z]+', '%20', title))
        else:
            authors=author.split(",")
            st = "t%3A({})".format(title)
            for a in authors:
                st=st+"%20"+"a%3A({})".format(a)
            aclibraryUrl = url.format(st)
        rs=requests.get(aclibraryUrl)
        soup = BeautifulSoup(rs.text, 'html.parser')
        link=soup.find(id="recordDisplayLink2Component")
        if link:
            detailUrl = "https://browse.nypl.org"+link["href"]
        else:
            detailUrl="None"

        sheet.write(j, 0, cudosid)
        sheet.write(j, 1, goodreadsid)
        sheet.write(j, 2, title)
        sheet.write(j,3,author)
        sheet.write(j, 4, goodreadsUrl)
        sheet.write(j, 5, aclibraryUrl)
        sheet.write(j, 6, detailUrl)
        file.save('New_York.xls')
        print(cudosid,goodreadsid,title,aclibraryUrl,detailUrl)