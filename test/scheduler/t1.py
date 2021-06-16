from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# BlockingScheduler

# year (int|str) – 4-digit year
# month (int|str) – month (1-12)
# day (int|str) – day of the (1-31)
# week (int|str) – ISO week (1-53)
# day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
# hour (int|str) – hour (0-23)
# minute (int|str) – minute (0-59)
# second (int|str) – second (0-59)
# start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
# end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
# timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='1', hour=15, minute=36)
scheduler.start()