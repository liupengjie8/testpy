from selenium import webdriver  # 导入selenium模块
import time  # 导入时间模块
from selenium.webdriver.support.select import Select

# 工时系统url
url = 'http://39.98.72.170:8212/Accounts/SignIn'
# 产品id
product_id = ''
# 用户名
user_name = ''
# 密码
password = ''
# 浏览器驱动
driver = webdriver.Chrome()


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


# 新增工作
def add_work_rec():
    driver.switch_to.frame("jerichotabiframe_1")
    input = driver.find_elements_by_tag_name("input")[7]
    input.click()
    time.sleep(2)
    # 获取alert对话框
    dig_alert = driver.switch_to.alert
    dig_alert.accept()
    time.sleep(2)
    driver.switch_to.frame("ifCreateDialog")
    time.sleep(2)
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
add_work_rec()
