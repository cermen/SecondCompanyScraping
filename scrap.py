from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains as ac

from selenium.common.exceptions import NoSuchElementException

import pandas as pd

from datetime import datetime
import time

from tkinter.filedialog import asksaveasfilename


# seamless 로그아웃
def logout(driver):
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div[2]/span/button').click()
    driver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div[2]/ul/li[6]/a').click()
    driver.close()


# 스크랩한 기업 삭제
def delete_companies(driver):
    wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                       '/html/body/div/div/div/div[2]/div/div[2]/table/thead/tr/th/div/span/div/div/div/label/span'))).click()
    time.sleep(1)
    wait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/span/button'))).click()
    time.sleep(1)
    wait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/ul/li/a'))).click()
    time.sleep(1)
    wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div/input'))).send_keys(
        'delete')
    time.sleep(1)
    wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div[2]/div/div/div[3]/button[2]'))).send_keys(
        Keys.ENTER)
    time.sleep(5)


def scrap(keyword, start_page, end_page, columns):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://login.seamless.ai/login')
    driver.set_window_size(1500, 1000)

    time.sleep(1)
    driver.find_element_by_name('username').send_keys('anastasia@planinfinit.com')
    driver.find_element_by_name('password').send_keys('1q2w3e$R%T')
    driver.find_element_by_css_selector('form > button').click()
    time.sleep(3)

    try:
        driver.get('https://login.seamless.ai/search/companies?page=' + str(
            start_page) + '&locations=1&companiesExactMatch=false&companyKeywords=' + keyword)
        driver.find_element_by_css_selector('button > svg').click()

        for p1 in range(start_page, end_page + 1):
            driver.find_element_by_css_selector('body').send_keys(Keys.HOME)
            time.sleep(5)

            # 페이지 전체 한꺼번에 스크랩
            wait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                               '/html/body/div/div/div/div[2]/div/div[2]/div[2]/table/thead/tr/th/div/span/div/div/div/label/span'))).click()
            time.sleep(1)
            wait(driver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/button'))).click()

            if p1 < end_page:
                driver.find_element_by_css_selector('body').send_keys(Keys.END)
                time.sleep(20)
                wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/button[2]'))).send_keys(
                    Keys.ENTER)
            else:
                time.sleep(10)

        # 스크랩한 기업 정보 가져오기
        all_data = list()  # 정보 저장할 리스트

        wait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div/div/div/div[3]/a'))).click()  # 스크랩한 기업 목록으로 넘어감
        time.sleep(5)

        item_info = wait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div/div/div[2]'))).text
        item_len = int(item_info.split()[-1])
        pages = (item_len - 1) // 15 + 1

        for p2 in range(pages):
            if p2 < pages - 1:
                items = 15
            else:
                items = item_len % 15 if item_len % 15 else 15

            for i in range(items):
                company_data = list()
                wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                   '/html/body/div/div/div/div[2]/div/div[2]/table/tbody/tr[' + str(
                                                                       i + 1) + ']/td[2]/div/div/button'))).send_keys(
                    Keys.ENTER)
                time.sleep(5)
                wait(driver, 60).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div/div[2]/button'))).send_keys(Keys.ENTER)
                time.sleep(5)

                wait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,
                                                                   '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/span/span/span[4]/span/span/a'))).send_keys(
                    Keys.ENTER)
                name = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]'))).text
                desc = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                          '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/span/span'))).text
                website = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div[2]'))).text
                industry = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[4]/div[2]'))).text
                size = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[5]/div[2]'))).text
                founded = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[6]/div[2]'))).text
                company_type = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[7]/div[2]'))).text
                revenue = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[8]/div[2]'))).text
                location = wait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[9]/div[2]'))).text

                company_data.extend([name, desc, website, industry, size, founded, company_type, revenue, location])
                all_data.append(company_data)

                time.sleep(20)

                driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)

                if i % 5 == 4:
                    time.sleep(1)
                    driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)

            time.sleep(1)
            driver.find_element_by_css_selector('body').send_keys(Keys.HOME)
            time.sleep(2)

            delete_companies(driver)

        all_columns = [
            'Company Name', 'Description', 'Website', 'Industry', 'Company Size', 'Founded', 'Company Type',
            'Revenue',
            'Location'
        ]
        all_data.reverse()
        all_data = pd.DataFrame(all_data, columns=all_columns, index=list(range(1, item_len + 1)))[columns]

        # file_type = [('엑셀 파일', '*.xlsx')]
        # file_name = asksaveasfilename(filetypes=file_type, defaultextension=str(file_type))
        # all_data.to_excel(file_name, encoding='utf-8-sig')

        now = datetime.today().strftime('%y%m%d_%H%M%S')

        file_name = 'seamless_{}_{}.xlsx'.format(keyword, now)
        all_data.to_excel(file_name, encoding='utf-8-sig')
    except Exception:
        time.sleep(1)
        driver.find_element_by_css_selector('body').send_keys(Keys.ESCAPE)
        time.sleep(1)
        wait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div/div/div/div[3]/a'))).click()  # 스크랩한 기업 목록으로 넘어감
        time.sleep(1)
        ac(driver).move_by_offset(0, 500).click().perform()
        time.sleep(5)

        try:
            item_info = wait(driver, 30).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'div.RecordCount__RecordCountContainer-jdtFHI'))).text
            item_len = int(item_info.split()[-1])
            pages = (item_len - 1) // 15 + 1
            for p in range(pages):
                delete_companies(driver)
        except NoSuchElementException:
            pass
    finally:
        logout(driver)
