from flask import Flask, render_template, url_for, request, jsonify
from flask_cors import CORS

# module
from module.hackmdAPI import get_hackmd_urls
from module.crawlerHackMD import crawlerHackMD

app = Flask(__name__)
CORS(app)


@app.route('/')
# def index():
#   return render_template('index.html')
@app.route('/SendAPI', methods=['POST'])
def SendAPI():
    API_data = request.get_json()
    print(API_data) 
    # get hackmqd urls
    urls = get_hackmd_urls(API_data)
    for url in urls:
        # windows 驅動程式 ， ubuntu 可能還要看一下怎麼啟動，因為解壓縮後不是執行檔
        chromeDriverPath = 'chromedriver.exe'
        # download markdown file > the markdown file will show up in the Download folder
        crawlerHackMD(url, chromeDriverPath)
    results = {'status': API_data}
    return jsonify(results)

if __name__ == "__main__":
  app.run(debug=True)