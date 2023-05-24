from PyHackMD import API
import urllib.request
import re
import os

# 一個筆記裡面的所有圖片儲存到本機
def saveImg(result):
    for imgURL in result:
        # 儲存圖片
        try:
            urllib.request.urlretrieve(imgURL, 'image/' + os.path.basename(imgURL))
        except:
            print("error on "+ imgURL)

def main():
    global api
    token = "26T3TUGVZ1GZO9I9JAQ8QRNKAF2XG8GGEHFOPGYVA7YJ07NT7N"
    api = API(token)
    # get all notes in token
    data = api.get_note_list()
    # 因為 API 有次數限制，所以先測試一個
    data = data[:1]

    imageURL = ["https://hackmd.io/_uploads","https://i.imgur.com"]
    num = 0
    for note in data:
        noteID = note['id']
        # 取得筆記的所有圖片網址
        content = api.get_note(noteID)["content"]
        for url in imageURL:
            # ^ 開頭要包含什麼（imageURL）()：對括弧內的字元形成群組？
            result = re.findall(url+"/[^\ (\n)]*", content)
            saveImg(result)
        # 紀錄目前已經備份了幾個共筆
        num += 1
        print('\r' + str(num) + '/' + str(len(data)), end='')

if __name__ == "__main__":
    if not os.path.exists('image'):
        os.makedirs('image')
    main()