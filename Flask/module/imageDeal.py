import re
import os
import urllib.request

# save the image by using url
def saveImage(imageURLs,savePath):
    for imgURL in imageURLs:
        try:
            print("~~~~~~~~~~~~",savePath + os.path.basename(imgURL))
            urllib.request.urlretrieve(imgURL, savePath + os.path.basename(imgURL))
        except:
            print("error on "+ imgURL)

# get all the url of image
def getImageURL(hackmd_prefix,content):
    # 共筆中所有的圖片網址
    imageURLs = []
    for url in hackmd_prefix:
        # 找符合 imageURL 網址的文字，^ 開頭要包含什麼（imageURL）()：對括弧內的字元形成群組？
        result = re.findall(url+"[^\ (\n)]*", content)
        imageURLs += result
    return imageURLs