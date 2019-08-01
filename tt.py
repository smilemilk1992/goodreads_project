# -*- coding: utf-8 -*-
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
str="ete the Cat: A Pet for Pete"
str1="Why Oh Why Are Deserts Dry?: All About Deserts"
str2="Why Oh Why Are (xxx)Deserts Dry?: All About Deserts"
str3="Pat the []Bunny (Pat the Bunny)"
str4="Brown Bear, Brown Bear, What Do You See?"
str5="No Means No!: Teaching Personal Boundaries, Consent; Empowering Children by Respecting Their Choices and Right to Say 'No!'"

print re.split("\?|:|!|\(",str3)[0]
print re.sub(",|!|\?|:|;|\|-|\[|\]|\(|\)", '', re.split("\?|:|!",str3)[0])

