from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc 
from time import sleep


def test_eight_components():
    options = uc.ChromeOptions() 
    options.headless = True
    driver = uc.Chrome() 

    driver.get("https://chat.openai.com/auth/login")
    driver.maximize_window() 
    sleep(3)

    # find button login
    log_in = driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]')
    log_in.send_keys(Keys.ENTER)
    sleep(3)

    # get and submit email
    driver.get(driver.current_url)
    email = driver.find_element(by=By.ID, value="username")
    email.send_keys('username@gmail.com')
    email.send_keys(Keys.ENTER)
    sleep(3)

    # get password submit form
    driver.get(driver.current_url)
    password = driver.find_element(by=By.ID, value="password")
    password.send_keys('password')
    password.send_keys(Keys.ENTER)
    sleep(3)
    # ------------- page chatgpt
    # skip modal
    driver.get(driver.current_url)
    sleep(3)
    next_button = driver.find_element(by=By.XPATH, value='//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button')
    next_button.click()
    sleep(2)
    next_button = driver.find_element(by=By.XPATH, value='//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')
    next_button.click()
    sleep(2)
    next_button = driver.find_element(by=By.XPATH, value='//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')
    next_button.click()
    sleep(2)

    # add textarea
    textarea = driver.find_element(by=By.ID, value='prompt-textarea')
    textarea.send_keys('Tyson Fury là ai')
    textarea.send_keys(Keys.ENTER)
    
    sleep(1000)

    driver.close()

test_eight_components()