import re
import os
import urllib.request

# save the image by using url
def saveImage(imageURLs,savePath):
    for imgURL in imageURLs:
        try:
            urllib.request.urlretrieve(imgURL, savePath + os.path.basename(imgURL))
        except:
            print("error on "+ imgURL)

# get all the url of image
def getImageURL(content):
    # 共筆中所有的圖片網址
    imageURLs = []
    # 目前共筆的網址 url 只有這兩個
    imageURL = ["https://hackmd.io/_uploads","https://i.imgur.com"]
    for url in imageURL:
        # 找符合 imageURL 網址的文字，^ 開頭要包含什麼（imageURL）()：對括弧內的字元形成群組？
        result = re.findall(url+"/[^\ (\n)]*", content)
        imageURLs += result
    return imageURLs