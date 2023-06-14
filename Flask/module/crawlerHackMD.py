import requests
from bs4 import BeautifulSoup

# 取得一個共筆的所有內容
def getContent(url):
    # 發 request 爬蟲取得該 url 的文字
    res = requests.get(url).text
    # 取得的 response 轉換成 html
    res_soup = BeautifulSoup(res, 'html.parser')
    return res_soup
