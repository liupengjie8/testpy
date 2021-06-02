import urllib.request
from bs4 import BeautifulSoup
import time

url = "https://www.aicoin.cn/?long_lives_aicoin=%22live%22"

def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    span = soup.find('span', attrs={'class', 'emphasis'})
    print(span.getText())


# 每n秒执行一次
def timer(n):
    while True:
        parse_html(get_html(url))
        time.sleep(n)
# 5s
timer(15)