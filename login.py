from setup import setup_driver
import argparse
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import getpass
import pickle
import os

def setup_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File đầu vào", required=True)
    parser.add_argument("-o", "--output", help="File đầu ra", required=True)
    args = parser.parse_args()

    return args

def login(driver):
    args = setup_command()

    if not os.path.exists(args.file) or not os.path.exists(args.output):
        print("Error: Tệp tin không tồn tại.")
        exit(1)

    if os.path.exists('cookies.pkl'):
        driver.get("https://chat.openai.com")

        cookies = pickle.load(open("cookies.pkl", "rb"))

        for cookie in cookies:
            # cookie_domain = cookie['domain']
            # if cookie_domain.startswith('.'):
            #     cookie_domain = cookie_domain[1:]

            cookie_secure = cookie.get('secure', False)
            cookie_http_only = cookie.get('httpOnly', False)            

            driver.add_cookie({
                'name': cookie['name'],
                'value': cookie['value'],
                # 'domain': cookie_domain,
                'path': cookie['path'],
                'secure': cookie_secure,
                'httpOnly': cookie_http_only,
                'expiry': 1687749438,
            })
        
        sleep(2)
        driver.get("https://chat.openai.com")
    else:
        try:
            email_input = input("Nhập địa chỉ email: ")
            password_input = getpass.getpass("Nhập mật khẩu: ")
        except KeyboardInterrupt:
            exit()

        driver.get("https://chat.openai.com")
        driver.maximize_window() 
        sleep(3)

        # find button login
        log_in = driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]')
        log_in.send_keys(Keys.ENTER)
        sleep(3)

        # get and submit email
        driver.get(driver.current_url)
        email = driver.find_element(by=By.ID, value="username")
        email.send_keys(email_input)
        email.send_keys(Keys.ENTER)
        sleep(3)

        try:
            error_email_msg = driver.find_element(by=By.XPATH, value='//*[@id="error-element-username"]')
            if error_email_msg.text:
                print('Error: Địa chỉ Email không chính xác, hãy chạy lai chương trình')
                exit()
        except NoSuchElementException:
            pass

        # get password submit form
        driver.get(driver.current_url)
        password = driver.find_element(by=By.ID, value="password")
        password.send_keys(password_input)
        password.send_keys(Keys.ENTER)
        sleep(3)

        try:
            error_password_msg = driver.find_element(by=By.XPATH, value='//*[@id="error-element-password"]')
            if error_password_msg.text:
                print('Error: Mật khẩu không chính xác, hãy chạy lại chương trình')
                exit()
        except NoSuchElementException:
            pass

        sleep(3)

        cookies = driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))

    return args
