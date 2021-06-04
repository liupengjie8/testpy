from selenium import webdriver#导入selenium模块
import time#导入时间模块

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('http://39.98.72.170:8212/Accounts/SignIn')#打开百度
input_text=driver.find_element_by_id("USERNAME")#通过id名来查找标签
input_text.send_keys('liupengjie')#往输入框里面输入查询字词
input_text=driver.find_element_by_id("INPUT_PASSWORD")#通过id名来查找标签
input_text.send_keys('123456')#往输入框里面输入查询字词
button=driver.find_element_by_class_name("login_btn")#通过id名来查找标签
button.click()#点击登录
time.sleep(3)#休眠5s为了看看效果

div=driver.find_element_by_class_name("divTopMenu")
a = div.find_elements_by_tag_name("a")[3]
a.click()

time.sleep(3)
driver.switch_to.frame("jerichotabiframe_1")

input = driver.find_elements_by_tag_name("input")[7]
input.click()

time.sleep(2)
# 获取alert对话框
dig_alert = driver.switch_to.alert
dig_alert.accept()


time.sleep(3)
driver.switch_to.frame("ifCreateDialog")

time.sleep(3)
select = driver.find_element_by_id('W_CHARACTER')
Select(select).select_by_visible_text('研发')

driver.find_element_by_class_name("m-input").click()

driver.find_elements_by_tag_name('li')[10].click()

driver.find_element_by_id('ID_OK').click()











# driver.quit()#退出浏览器
