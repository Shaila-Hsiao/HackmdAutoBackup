from PyHackMD import API
import re

# update the content to HackMD
def update(token,markdown,note_id):
    api = API(token)
    # FIXME: 測試用：開一個空白共筆寫入
    note_id = "deVGtwP8SY-Dy_Zt-jTVUQ"
    # update the content of note
    result = api.update_note(note_id, content='')
    result = api.update_note(note_id, content=markdown)
    print("modify status:",result)
    # return result # 顯示 Accept: 成功修改

# hackmd 的圖片網址換成 wordpress 圖片網址
def replaceRule(markdown,wp_img_name,wp_img_url):
    for i in range(len(wp_img_name)):
        # 找到此圖片原本的 hackmd 網址
        hackmd_img_url = re.findall("https[^*\ ()]*"+wp_img_name[i], markdown)
        # replace hackmd url with wordpress url 
        for url in hackmd_img_url:
            markdown = markdown.replace(url,wp_img_url[i])
    return markdown

# get user's url of notes
def get_hackmd_urls(token):
    api = API(token)
    # get all notes in token
    data = api.get_note_list()
    # FIXME: test
    data = data[:1]
    # get url of notes
    urls = []
    # get id of notes
    note_id_list = []

    for i in range(len(data)):
        noteURL = data[i]['publishLink']
        node_id = data[i]["id"]
        urls.append(noteURL)
        note_id_list.append(node_id)
    return urls,note_id_list
# use HackMD API for getting content of note
def get_hackmd_content(token,note_id):
    api = API(token)
    data = api.get_note(note_id)
    return data["content"]
