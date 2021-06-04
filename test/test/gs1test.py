import datetime
import chinese_calendar

a = datetime.datetime.today()

is_workday = chinese_calendar.is_workday(a)
if is_workday:
    print(1)
else:
    print(2)