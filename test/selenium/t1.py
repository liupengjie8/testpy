from selenium import webdriver#导入selenium模块
import time#导入时间模块
driver = webdriver.Chrome()
driver.get('http://39.98.72.170:8212/Accounts/SignIn')#打开百度
input_text=driver.find_element_by_id("USERNAME")#通过id名来查找标签
input_text.send_keys('liupengjie')#往输入框里面输入查询字词
input_text=driver.find_element_by_id("INPUT_PASSWORD")#通过id名来查找标签
input_text.send_keys('123456')#往输入框里面输入查询字词
button=driver.find_element_by_class_name("login_btn")#通过id名来查找标签
button.click()#点击登录
time.sleep(5)#休眠5s为了看看效果

# div=driver.find_element_by_class_name("divTopMenu")
# a = div.find_elements_by_tag_name("a")[3]
# a.click()


driver.get('http://39.98.72.170:8212/WorkNotes/WorkNoteIndex')
input = driver.find_elements_by_tag_name("input")[7]
input.click()

time.sleep(1)
# 获取alert对话框
dig_alert = driver.switch_to.alert

# 打印警告对话框内容
print(dig_alert.text)
# alert对话框属于警告对话框，我们这里只能接受弹窗
dig_alert.accept()


print(input.text)
# driver.quit()#退出浏览器
