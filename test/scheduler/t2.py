from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=87032723645bb2fb701f33242b6afce88cb1fd79702ca2e6e3fce26f2ca0dd99 '
secret = 'SECadabb2482dcade23f888ea30ee532eded7add910838d87b4436369d76bb94a82'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)

# 输出时间
def job1():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    xiaoding.send_text(msg='今天是周五，别忘了工时填报！',is_at_all=True)

def job2():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    xiaoding.send_text(msg='今天是周五，别忘了提交周报！',is_at_all=True)

scheduler = BlockingScheduler()
scheduler.add_job(job1, 'cron', day_of_week='4', hour=9, minute=10)
scheduler.add_job(job2, 'cron', day_of_week='4', hour=17, minute=50)
scheduler.start()