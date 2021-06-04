import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://39.98.72.170:8212/WorkNotes/GetUserWorkTaskToDay?DATE=2021-06-03"
data = {
"WorkNoteCreateTS": "5539cd17617749ce9c33798ed2d59d89",
"WORK_DATE": "2021-06-03",
"W_CHARACTER": "研发",
"AMORTIZE_WAY": "产品",
"PRODUCT_ID": "666210300017",
"TASK_TIME_DAY": "1.0"
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
print(html)