from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    os.system("python work_rec_submit_lpj.py")
    os.system("python work_rec_submit_gy.py")
    os.system("python work_rec_submit_lm.py")
    os.system("python work_rec_submit_ly.py")

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='4', hour=9, minute=20)
scheduler.start()