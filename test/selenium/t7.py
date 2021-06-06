from selenium import webdriver  # 导入selenium模块
import time  # 导入时间模块
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support.select import Select
import datetime
from datetime import timedelta
import json

# 工时系统url
url = 'http://39.98.72.170:8212/Accounts/SignIn'
# 产品id
product_id = '666210300018'
# 用户名
user_name = 'liupengjie'
# 密码
password = '123456'
# 浏览器驱动
driver = webdriver.Chrome()
# 本周工作日
work_days = []


def get_work_day():
    holidays = json.load(open('holiday.json', "rb"))["holidays"]
    now = datetime.datetime.now()
    this_week_start = now - timedelta(days=now.weekday())
    this_week_dates = [this_week_start, this_week_start + timedelta(1), this_week_start + timedelta(2),
                       this_week_start + timedelta(3),
                       this_week_start + timedelta(4), this_week_start + timedelta(5), this_week_start + timedelta(6)]
    for day in this_week_dates:
        day_str = str(day).split()[0]
        if day_str not in holidays:
            work_days.append(day_str)


# 登录
def do_login():
    driver.get(url)
    input_text = driver.find_element_by_id("USERNAME")
    input_text.send_keys(user_name)
    input_text = driver.find_element_by_id("INPUT_PASSWORD")
    input_text.send_keys(password)
    button = driver.find_element_by_class_name("login_btn")
    button.click()


# 打开工作记录
def to_work_rec():
    div = driver.find_element_by_class_name("divTopMenu")
    a = div.find_elements_by_tag_name("a")[3]
    a.click()
    time.sleep(2)
    driver.switch_to.frame("jerichotabiframe_1")
    try:
        inputs = driver.find_elements_by_xpath("//input[@title='删除']")
        for input in inputs:
            input.click()
            driver.switch_to.alert.accept()
    except NoSuchElementException:
        print("alert 没找到1")
    finally:
        print(121)


# 新增工作
def add_work_rec(day):
    try:
        input = driver.find_elements_by_tag_name("input")[7]
        input.click()
        time.sleep(2)
        # 获取alert对话框
        driver.switch_to.alert.accept()
        time.sleep(2)

    except NoAlertPresentException:
        print("alert 没找到2")
    finally:
        driver.switch_to.frame("ifCreateDialog")
        time.sleep(2)
        input_text = driver.find_element_by_id("WORK_DATE")
        input_text.clear()
        input_text.send_keys(day)
        select = driver.find_element_by_id('W_CHARACTER')
        Select(select).select_by_visible_text('研发')
        driver.find_element_by_class_name("m-input").click()
        product_lis = driver.find_elements_by_tag_name('li')
        for li in product_lis:
            if li.get_attribute("data-value") == product_id:
                li.click()
        driver.find_element_by_id('ID_OK').click()


do_login()
time.sleep(3)
to_work_rec()
time.sleep(3)
get_work_day()
for day in work_days:
    time.sleep(2)
    print(day)
    add_work_rec(day)
