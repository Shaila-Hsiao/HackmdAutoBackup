from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from os import walk
from os.path import join
import json



# Login
with open('account.json', 'r', encoding='utf-8') as f:
    account = json.load(f)

id = account['user']
password = account['password']

url = 'http://shaila.org/xmlrpc.php'

which = 'publish'

client = Client(url, id, password)
# 需要檢查的資料夾路徑
mypath = "/home/shaila/LSA/Upload/Image"
# 照片路徑list
ImgPath = []
# 照片名稱list
ImgName = []
# 存入照片路徑與名稱
for root, dirs, files in walk(mypath):
  for f in files:
    fullpath = join(root, f)
    ImgPath.append(fullpath)
    ImgName.append(f)
    print("filesPath 【",f,"】 : ",fullpath)
    print(ImgPath)
    print(ImgName)

# 依續將資料夾內所有照片上傳至wordpress
for i in range(len(ImgPath)):
    # set to the path to your file
    filename = ImgPath[i]
    print("filename",filename)
    # prepare metadata
    data = {
            'name': ImgName[i],
            'type': 'image/jpeg',  # mimetype
    }
    print(data)
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    # response type : dict
    # 印出 url
    print("url",response['url'])
    attachment_id = response['id']

