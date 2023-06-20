from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep
from setup import setup_driver
from login import login
from docx import Document
import pyperclip
import pyfiglet
import os

def create_table_docx(questions, answers, output_path):
    document = Document()
    table = document.add_table(rows=1, cols=2)
    table.style = 'Table Grid'

    heading_cells = table.rows[0].cells
    heading_cells[0].text = 'Question'
    heading_cells[1].text = 'Answer'

    for question, answer in zip(questions, answers):
        row_cells = table.add_row().cells
        row_cells[0].text = question
        row_cells[1].text = answer

    document.save(output_path)

def chatgpt_crawler():
    ascii_banner = pyfiglet.figlet_format("ChatGPT Crawler")
    print(ascii_banner)
    try:
        driver = setup_driver()
        args = login(driver)

        # skip modal
        sleep(1)
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button')))
        next_button.click()

        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')))
        next_button.click()

        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')))
        next_button.click()

        # add textarea
        textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))

        # read file
        _, ext = os.path.splitext(args.file)
        if ext.lower() != '.txt':
            raise ValueError(f"File phải có đuôi .txt")
        else:
            try:
                with open(args.file, 'r', encoding='utf-8') as file:
                    questions = file.readlines()
                    questions = [value.strip() for value in questions if value.strip()]
            except Exception as e:
                print(f"Có lỗi xảy ra khi mở file: {e}")

            if not questions:
                print("Error: Tệp tin không có dữ liệu.")
                exit(1)

            answers = []
            for question in questions:
                textarea.send_keys(question)
                textarea.send_keys(Keys.ENTER)

                try:
                    button_continue_generating = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button[2]')))
                    button_continue_generating.click()
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass

                button_copy = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/div/div/div//div[contains(., "{question}")]/following-sibling::div[1]/div/div[2]/div[2]/div/button')))
                button_copy.click()
                answers.append(pyperclip.paste())

            create_table_docx(questions=questions, answers=answers, output_path=args.output)
            print('Crawl thông tin thành công')
            sleep(2)

    # except Exception as e:
    #     print(f"Có lỗi xảy ra: {e}")
    finally:
        if driver is not None:
            driver.quit()

chatgpt_crawler()
