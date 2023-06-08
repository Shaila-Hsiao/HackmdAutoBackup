from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 讓我們可以按鍵盤上的按鍵
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import requests
from bs4 import BeautifulSoup

# 取得一個共筆的所有內容
def getContent(url):
    # 發 request 爬蟲取得該 url 的文字
    res = requests.get(url).text
    # 取得的 response 轉換成 html
    res_soup = BeautifulSoup(res, 'html.parser')
    return res_soup

def crawlerHackMD(url, driverPath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # 關閉 GPU 避免某些系統或是網頁出錯
    options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖片，提升速度
    options.add_argument('--no-sandbox')  # 以最高權限執行
    options.add_argument("--disable-javascript")  # 禁用 JavaScript
    prefs = {
        'profile.default_content_setting_values':  {
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=options, service=Service(driverPath))
    driver.get(url)
    time.sleep(5)

    # click other button
    WebDriverWait(driver, 50).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME,'rounded.ui-menu.navbar-button-icon'))
        )
    otherBtn = driver.find_element(By.CLASS_NAME,'rounded.ui-menu.navbar-button-icon')
    otherBtn.click()
    time.sleep(3)

    # click download markdon
    WebDriverWait(driver, 50).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'ui-download-markdown'))
        )
    downloadMD = driver.find_element(By.CLASS_NAME,'ui-download-markdown')
    downloadMD.click()
    time.sleep(3)
    driver.quit()

