from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.posts import NewPost,EditPost
from bs4 import BeautifulSoup
from os import walk
from os.path import join

#Update Content
def UpdateWP(post_id,account,wp_password,wp_url,html):
  id = account
  password = wp_password
  url = 'http://'+wp_url+'/xmlrpc.php'
  client = Client(url, id, password)
  result = client.call(EditPost(post_id, {'post_content': html}))
  #Returns: True on successful edit.
  return result


#上傳內文
def CreateWP(account,wp_password,wp_url,html,title,tag):
  id = account
  password = wp_password

  url = 'http://'+wp_url+'/xmlrpc.php'
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
  global media
  # 登入帳號、密碼
  id = account
  password = wp_password
  # wp_url : 
  url = 'http://'+wp_url+'/xmlrpc.php'
  client = Client(url, id, password)
  # 呼叫GetMediaLibrary方法獲取媒體庫中的圖片資訊 media = []
  try:
    exsist_media = client.call(media.GetMediaLibrary({'mime_type':"image/png" }))
  except:
    print("first upload")
  exsist_WPImg = []
  for item in exsist_media:
    exsist_WPImg.append(item.title)
  # 照片路徑list
  ImgPath = []
  # 照片名稱list
  ImgName = []
  wp_img_name = []
  wp_img_url = []
  for root,dirs ,files in walk(savePath):
    for f in files:
      fullpath = join(root, f)
      if f in exsist_WPImg:
        print("exsist Image")
      else:
        ImgPath.append(fullpath)
        ImgName.append(f)
        print("filesPath 【",f,"】 : ",fullpath)

  # 依續將資料夾內所有照片上傳至wordpress
  for i in range(len(ImgPath)):
    # set to the path to your file
    filename = ImgPath[i]
    # prepare metadata
    data = {
            'name': ImgName[i],
            'type': 'image/png',  # mimetype
    }
    print(data)
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
    try:
      response = client.call(media.UploadFile(data))
      # 印出 url
      wp_img_name.append(response['file'])
      wp_img_url.append(response['url'])
      print("url",response['url'])
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

