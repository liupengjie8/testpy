import datetime
from datetime import timedelta

now = datetime.datetime.now()

dayOfWeek = now.weekday()+1
week_start = now - timedelta(days=now.weekday())
week_end = now + timedelta(6-now.weekday())

days = [week_start, week_start+timedelta(1), week_start+timedelta(2), week_start+timedelta(3), week_start+timedelta(4), week_start+timedelta(5), week_start+timedelta(6)]

for day in days:
    print(str(day).split()[0])

if dayOfWeek == 7:
    print(1)
else:
    print(0)
