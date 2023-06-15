from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. Khai bao bien browser
browser = webdriver.Chrome()

# 2. Mo thu 1 trang we
browser.get("http://facebook.com")

# 2a. Dien thong tin vao o user va pass
txtUser = browser.find_element(by=By.XPATH, value="//input[@type='text' and @name='email']")
txtUser.send_keys('kieuthanhnam.999@gmail.com')

txtPass = browser.find_element(by=By.XPATH, value="//input[@type='password' and @name='pass']")
txtPass.send_keys('143Henry!')

# 2b. Submit form
txtPass.send_keys(Keys.ENTER)

sleep(5)

# 4. Dong trinh duyet
browser.close()