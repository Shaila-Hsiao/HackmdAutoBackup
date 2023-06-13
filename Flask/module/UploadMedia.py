from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import NewPost
from bs4 import BeautifulSoup
from os import walk
from os.path import join
import json


#上傳內文
def UpdateWP(account,wp_password,wp_url,html):
  id = account
  password = wp_password

  url = 'http://'+wp_url+'/xmlrpc.php'
  # 找 title
  soup = BeautifulSoup(html, 'html.parser')
  title = soup.h1.string
  tag = soup.code.string
  which = 'publish'
  wp = Client(url, id, password)
  post = WordPressPost()
  post.post_status = which
  post.title = title
  post.content = html
  post.excerpt = 'API TEST EXCERPT'
  post.terms_names = {
      "post_tag": [tag],
      "category": ['test']
  }

  wp.call(NewPost(post))

  print("Update content")

# 上傳照片
def UploadImage(account,wp_password,wp_url,savePath):
  # Login
  # with open('account.json', 'r', encoding='utf-8') as f:
  #     account = json.load(f)
  # 登入帳號、密碼
  id = account
  password = wp_password
  # wp_url : 
  url = 'http://'+wp_url+'/xmlrpc.php'

  which = 'publish'

  client = Client(url, id, password)
  # 照片路徑list
  ImgPath = []
  # 照片名稱list
  ImgName = []
  wp_img_name = []
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
      # 印出 url
      print("url",response['url'])
      wp_img_name.append(response['file'])
      wp_img_url.append(response['url'])
      print("url",response['url'])
      attachment_id = response['id']
    except:
       print("error")
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    # response type : dict
  return wp_img_name,wp_img_url

