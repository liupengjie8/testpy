from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=4fb919b05bde12a70d7dcf4f9ddaf9e9dfee5cf82a23802fd82a27f00f3a77fe'
secret = 'SECf50a9ff48267e2669b9402ad8a637f9219053e49eee3783a7c7f42feb42af86c'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）

xiaoding.send_text(msg='欢迎欢迎！')

