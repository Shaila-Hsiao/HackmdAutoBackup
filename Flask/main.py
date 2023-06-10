from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS
import os

# module
from module.hackmdAPI import get_hackmd_urls, replaceRule, update, get_hackmd_content
from module.crawlerHackMD import crawlerHackMD, getContent
from module.imageDeal import saveImage, getImageURL
from module.UploadMedia import UploadImage
app = Flask(__name__)
CORS(app)
# 創建資料夾儲存圖片
if os.path.exists('./static') == False:
    os.makedirs('./static')
if os.path.exists('./static/image') == False:
    os.makedirs('./static/image')

@app.route('/')
# def index():
#   return render_template('index.html')
@app.route('/SendAPI', methods=['POST'])
def SendAPI():
    API_data = request.json['API_data']
    # Wordpress account、password、url
    account = request.json['account']
    wp_password = request.json['wp_password']
    wp_url = request.json['wp_url']
    print(API_data,account,wp_url,wp_password) 
    # get hackmqd urls
    urls, note_id_list = get_hackmd_urls(API_data)
    # FIXME: 測試用：已經完成了多少共筆的圖片備份
    num = 0
    for i in range(len(urls)):
        wp_img_name, wp_img_url = [],[] 
        # 共筆內圖片的前綴網址
        hackmd_prefix = ["https://hackmd.io/_uploads/","https://i.imgur.com/"]
        '''
        # windows 驅動程式 ， ubuntu 可能還要看一下怎麼啟動，因為解壓縮後不是執行檔
        chromeDriverPath = 'chromedriver.exe'
        # download markdown file -> the markdown file will show up in the Download folder
        crawlerHackMD(url, chromeDriverPath)
        '''
        # 取得共筆網頁內容
        res_soup = getContent(urls[i])
        # FIXME: 測試用： 查看共筆標題
        print("note url =",urls[i])
        print("title =",res_soup.head.title)
        # user's notes is public
        try:
            # get markdown content html
            html = res_soup.find("div",class_="container-fluid markdown-body")
            markdown = html.get_text()
            f = open("test.txt","w")
            f.write(html)
            f.close
            print("===>",type(markdown))
        # if the user's notes is forbidden
        except:
            # use HackMD API
            markdown = get_hackmd_content(API_data,note_id_list[i])
            print("===>",type(markdown))
        # 取得共筆內容的所有圖片網址
        imageURLs = getImageURL(hackmd_prefix,markdown)
        # 將圖片儲存到 ./static/image (注意：最後一定要加個斜線)
        savePath = "./static/image/"
        saveImage(imageURLs,savePath)
        num += 1
        print('\r' + str(num) + '/' + str(len(urls)), end='')
        # 上傳照片，取得照片在 wordpress 的 URL
        wp_img_name, wp_img_url = UploadImage(account,wp_password,wp_url,savePath)
        print("wp_img_url : ",wp_img_url)
        # HackMD 圖片網址換成 wordpress 網址
        content = replaceRule(markdown,hackmd_prefix,wp_img_name,wp_img_url)
        # 更新內容到 HackMD
        update(API_data,content,note_id_list[i])
    results = {'status': API_data}
    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=True)