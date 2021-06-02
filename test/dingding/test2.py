# coding:utf-8
import base64
import hashlib
import hmac
import json
import queue

import urllib.request

# 1、构建url
import time

import self as self
from dingtalkchatbot.chatbot import is_py3, quote_plus
from numpy import long


webhook = 'https://oapi.dingtalk.com/robot/send?access_token=ebc7aefccee9ff16fccc542d4765a38b69845eef38398952e9cedcccb9be5ea9'
secret = 'SEC675c4cb90f3a31298c28e5571e92bacd2ce6b8e6da3f05f78db8aedd6d3500dc'  #
# url为机器人的webhook

# 2、构建一下请求头部

header = {

    "Content-Type": "application/json",

    "Charset": "UTF-8"

}

# 3、构建请求数据

data = {
    "msgtype": "text",
    "text": {
        "content": "汪汪汪"
    },
    "at": {
         "isAtAll": False     #@全体成员（在此可设置@特定某人）
    }
}



def update_webhook(webhook=None):
    """
    钉钉群自定义机器人安全设置加签时，签名中的时间戳与请求时不能超过一个小时，所以每个1小时需要更新签名
    """
    start_time = time.time()
    if is_py3:
        timestamp = round(start_time * 1000)
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), digestmod=hashlib.sha256).digest()
    else:
        timestamp = long(round(start_time * 1000))
        secret_enc = bytes(secret).encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()

    sign = quote_plus(base64.b64encode(hmac_code))
    return '{}&timestamp={}&sign={}'.format(webhook, str(timestamp), sign)

# 4、对请求的数据进行json封装
sendData = json.dumps(data)  # 将字典类型数据转化为json格式
sendData = sendData.encode("utf-8")  # python3的Request要求data为byte类型
# 5、发送请求
request = urllib.request.Request(update_webhook(webhook), data=sendData, headers=header)
opener = urllib.request.urlopen(request)

#7、打印返回的结果
print(opener.read())