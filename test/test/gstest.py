import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
e = pd.bdate_range('6/1/2021', '6/30/2021')
print(e)

base_url = "http://39.98.72.170:8212/WorkNotes/StatisticsWorkTimeByCompleteness"
data = {
    "REAL_NAME": "刘鹏杰",
    "YEAR_MONTH": "202106"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=ebfjlyvh1izsnsl4emvwb3ys"
}
postdata = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request(url=base_url, headers=headers, data=postdata, method='POST')
response = urllib.request.urlopen(req)
html = response.read()
# html=response.read().decode('utf-8')  #这里讲解一下decode()是把bytes转化解码为了 str ,
# 但是写入文本的话，是不需要解码的，解码了str写不进去，
soup = BeautifulSoup(html, 'html.parser').getText()
print(soup)