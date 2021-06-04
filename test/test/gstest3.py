import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd


base_url = "http://39.98.72.170:8212/WorkNotes/GetUserWorkTaskToDay?DATE=2021-06-03"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=ebfjlyvh1izsnsl4emvwb3ys"
}

req = urllib.request.Request(url=base_url, headers=headers, method='GET')
response = urllib.request.urlopen(req)
html = response.read()
print(html)