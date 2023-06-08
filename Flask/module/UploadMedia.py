from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from os import walk
from os.path import join
import json

# 上傳照片
def  UploadImage(savePath):
  # Login
  with open('account.json', 'r', encoding='utf-8') as f:
      account = json.load(f)
  # 登入帳號、密碼
  id = account['user']
  password = account['password']

  url = 'http://shaila.org/xmlrpc.php'

  which = 'publish'

  client = Client(url, id, password)
  # 照片路徑list
  ImgPath = []
  # 照片名稱list
  ImgName = []
  wp_img_url = []
  # 存入照片路徑與名稱
  for root, dirs, files in walk(savePath):
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
    try:
      response = client.call(media.UploadFile(data))
      wp_img_url.append(response['url'])
    except:
       print("error")
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    # response type : dict
    # 印出 url
    attachment_id = response['id']
  print("url",response['url'])
  return wp_img_url

