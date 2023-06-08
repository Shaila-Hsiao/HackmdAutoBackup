import re
import os
import urllib.request

def saveImage(imageURLs,savePath):
    for imgURL in imageURLs:
        # 儲存圖片
        try:
            urllib.request.urlretrieve(imgURL, savePath + os.path.basename(imgURL))
        except:
            print("error on "+ imgURL)

def getImageURL(content):
    imageURLs = []
    imageURL = ["https://hackmd.io/_uploads","https://i.imgur.com"]
    for url in imageURL:
        # ^ 開頭要包含什麼（imageURL）()：對括弧內的字元形成群組？
        result = re.findall(url+"/[^\ (\n)]*", content)
        imageURLs += result
    return imageURLs