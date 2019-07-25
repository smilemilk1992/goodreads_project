# https://www.aclibrary.org/home
# http://encore.aclibrary.org/iii/encore/search/C__SThe%20Grumpus%20Under%20the%20Rug?lang=eng
#http://encore.aclibrary.org/iii/encore/search/C__St%3A%28Goldilocks%20and%20the%20Three%20Bears%29%20a%3A%28Sarah%20Delmege%29__Orightresult__U?lang=eng&suite=def
#http://encore.aclibrary.org/iii/encore/search/C__St%3A%28Goldilocks%20and%20the%20Three%20Bears%29%20a%3A%28Sarah%20Delmege%29%20a%3A%28Gavin%20Scott%29__Orightresult__U?lang=eng&suite=def
# http://encore.aclibrary.org/iii/encore/record/C__Rb2110882__SBeastly%20Babies__Orightresult__X6?lang=eng&suite=def

#t:(Goldilocks and the Three Bears) a:(Sarah Delmege) a:(Gavin Scott)
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
url="http://encore.aclibrary.org/iii/encore/search/C__S{}__Orightresult?lang=eng"
colum=["cudosid","goodreadsid","title","author","goodreadsUrl","aclibraryUrl","detailUrl"]
file=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=file.add_sheet("Alameda",cell_overwrite_ok=True)
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
            JSESSIONID=re.search(";jsessionid=.*?\?",link["href"]).group(0)
            detailUrl = "http://encore.aclibrary.org"+link["href"].replace(JSESSIONID,"?")
        else:
            detailUrl="None"

        sheet.write(j, 0, cudosid)
        sheet.write(j, 1, goodreadsid)
        sheet.write(j, 2, title)
        sheet.write(j,3,author)
        sheet.write(j, 4, goodreadsUrl)
        sheet.write(j, 5, aclibraryUrl)
        sheet.write(j, 6, detailUrl)
        file.save('Alameda.xls')
        print(cudosid,goodreadsid,title,aclibraryUrl,detailUrl)

