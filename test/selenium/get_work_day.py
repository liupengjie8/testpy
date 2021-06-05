import datetime
from datetime import timedelta
import json

path = 'holiday.json'
file = open(path, "rb")
fileJson = json.load(file)  # 剩下的就是解析了，都是列表和字典的操作
holidays = fileJson["holidays"]

now = datetime.datetime.now()

dayOfWeek = now.weekday() + 1
this_week_start = now - timedelta(days=now.weekday())
this_week_end = now + timedelta(6 - now.weekday())

this_week_dates = [this_week_start, this_week_start + timedelta(1), this_week_start + timedelta(2),
                  this_week_start + timedelta(3),
                  this_week_start + timedelta(4), this_week_start + timedelta(5), this_week_start + timedelta(6)]
work_days = []
for day in this_week_dates:
    day_str = str(day).split()[0]
    if day_str not in holidays:
        work_days.append(day_str)

print(work_days)
