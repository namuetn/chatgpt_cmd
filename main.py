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

def remove_first_line(answer):
    lines = answer.split('\n')

    first_line = lines[0]
    # Kiểm tra và loại bỏ dòng đầu tiên nếu chứa các từ "tóm tắt", "dưới đây" hoặc "sau đây"
    if any(word in first_line.lower() for word in ["tóm tắt", "dưới đây", "sau đây", ":"]):
        lines = lines[1:]

    result = '\n'.join(lines)  # Kết hợp lại các dòng còn lại thành một đoạn văn bản

    return result

def chatgpt_crawler():
    ascii_banner = pyfiglet.figlet_format("ChatGPT Crawler")
    print(ascii_banner)
    print('                                               -- Created by Kieu Thanh Nam -- \n')
    try:
        driver = setup_driver()
        args = login(driver)
        print("Đăng nhập thành công")

        # skip modal
        sleep(1)
        try:
            next_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button')))
            next_button.click()

            next_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')))
            next_button.click()

            next_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:r9:"]/div[2]/div[1]/div[2]/button[2]')))
            next_button.click()
        except TimeoutException:
            driver.refresh()

        # add textarea
        textarea = WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))

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
                print(f'Question: {question}')
                textarea.send_keys(question)
                textarea.send_keys(Keys.ENTER)
                print('+ Đang thu thập câu trả lời...')
                try:
                    WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, '//div[contains(@class, "text-2xl")]')))
                    button_continue_generating = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/main/div[3]/form/div/div[1]/div/button[2]')
                    button_continue_generating.click()
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass

                button_copy = WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="__next"]/div[1]/div[2]/div/main/div[2]/div/div/div//div[contains(., "{question}")]/following-sibling::div[1]/div/div[2]/div[2]/div/button')))
                driver.execute_script("arguments[0].scrollIntoView(true);", button_copy)
                button_copy.click()

                answer = pyperclip.paste()

                answers.append(remove_first_line(answer=answer))
                print("+ Thu thập thành công")
                sleep(1)


            create_table_docx(questions=questions, answers=answers, output_path=args.output)
            print('Success: Crawl thông tin thành công')

    except Exception as e:
        print(f"Có lỗi xảy ra, vui lòng crawl lại")
    finally:
        if driver is not None:
            driver.quit()

chatgpt_crawler()
