from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import time
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    os.system("python work_rec_submit_lpj.py")
    time.sleep(1)
    os.system("python work_rec_submit_gy.py")
    time.sleep(1)
    os.system("python work_rec_submit_lm.py")
    time.sleep(1)
    os.system("python work_rec_submit_ly.py")

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='4', hour=9, minute=40)
scheduler.start()