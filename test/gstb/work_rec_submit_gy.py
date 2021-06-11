from selenium import webdriver  # 导入selenium模块
import time  # 导入时间模块
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support.select import Select
import datetime
from datetime import timedelta
import json
from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=87032723645bb2fb701f33242b6afce88cb1fd79702ca2e6e3fce26f2ca0dd99 '
secret = 'SECadabb2482dcade23f888ea30ee532eded7add910838d87b4436369d76bb94a82'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）

# 工时系统url
url = 'http://39.98.72.170:8212/Accounts/SignIn'
# 产品id
product_id = '666210300020'
# 用户名
user_name = 'gaoya'
# 密码
password = '123456'
# 浏览器驱动
driver = webdriver.Chrome()
# 已经填报的工作日
hava_data_day = []
# 消息
msg = []


# 获取本周工作日
def get_work_day():
    # 本周工作日
    work_days = []
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
    return work_days


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
    driver.switch_to.frame("jerichotabiframe_1")


# 获取本周已经填写的工时
def get_finished_days():
    table = driver.find_element_by_id("tbResult")
    tds = table.find_elements_by_tag_name("td")
    for td in tds:
        if td.text in get_work_day():
            hava_data_day.append(td.text)
    if len(set(hava_data_day))==0:
        msg.append('填报前：本周未填写工时！')
    else:
        msg.append('填报前：本周已填写工时日期：' + str(set(hava_data_day)))
    myset = set(hava_data_day)
    for item in myset:
        if hava_data_day.count(item)>1:
            msg.append("其中：日期 %s 重复填写 %d次，请登录系统自行删除" % (item, hava_data_day.count(item)))


# 新增工作
def add_work_rec(work_days):
    i = 0
    d = []
    for index, day in enumerate(work_days):
        if day > str(datetime.datetime.now()).split()[0]:
            msg.append('填报日期'+day+'大于当前日期'+str(datetime.datetime.now()).split()[0]+'，无法填报！')
        else:
            if day not in hava_data_day:
                d.append(day)
                msg.append('检测到日期：' + day + '未填报')
                input = driver.find_elements_by_tag_name("input")[7]
                input.click()
                time.sleep(5)
                if i < 3:
                    # 获取alert对话框
                    dig_alert = driver.switch_to.alert
                    dig_alert.accept()
                time.sleep(2)
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
                driver.switch_to.parent_frame()
                i += 1
                msg.append('日期：' + day + '填报成功')
    if i == 0:
        msg.append('本周可填报日期都填报完成！')
    else:
        msg.append("填报完成，填报成功"+str(i)+"天，分别为：" + str(d))
    msg.append('程序执行完成，关闭浏览器！欢迎再次使用！')


# 发送操作日志
def send_log(msg):
    mkd_str = ''
    for m in msg:
        mkd_str += '\n* ' + m
    xiaoding.send_markdown('研发工时填报结果',
                           "# 用户工时填报详情：\n## 用户名："+user_name + mkd_str)


msg.append('本周需填写工时日期：' + str(get_work_day()))
do_login()
time.sleep(3)
to_work_rec()
time.sleep(3)
get_finished_days()
add_work_rec(get_work_day())
# 关闭浏览器
driver.close()
send_log(msg)
