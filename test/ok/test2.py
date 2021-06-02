import urllib.request
from bs4 import BeautifulSoup
from threading import Timer
import json
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=4fb919b05bde12a70d7dcf4f9ddaf9e9dfee5cf82a23802fd82a27f00f3a77fe'
secret = 'SECf50a9ff48267e2669b9402ad8a637f9219053e49eee3783a7c7f42feb42af86c'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
url = "https://www.ouyi.cc/priapi/v5/public/markets/important-index?t=1622610543452"


def get_html(urls):
    request = urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=urls, headers=headers)
    html = request.urlopen(req).read().decode()
    return html


def parse_html(file):
    soup = BeautifulSoup(file, 'html.parser').getText()
    json_obj = json.loads(soup)
    return json_obj["data"][0]["askPx"]

# 每n秒执行一次
def timer(n):
    while True:
        xiaoding.send_text(msg=parse_html(get_html(url)))
        time.sleep(n)
# 5s
timer(8)



