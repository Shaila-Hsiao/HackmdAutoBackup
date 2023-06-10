from PyHackMD import API

# update the content to HackMD
def update(token,html,note_id):
    api = API(token)
    # FIXME: 測試用：開一個空白共筆寫入
    note_id = "YNgKU6mkS6a4v6bKwomqpw"
    # update the content of note
    result = api.update_note(note_id, content=html)
    print("modify status:",result)
    # return result # 顯示 Accept: 成功修改

def replaceRule(markdown,prefix,wp_img_name,wp_img_url):
    for i in range(len(wp_img_name)):
        # 目前共筆內有的前綴網址 （ex: https://hackmd.io/_uploads/）
        for url in prefix:
            # 共筆連結
            url = url + wp_img_name[i]
            # 共筆內有此 HackMD 連結，就把 WordPress 連結取代
            if url in markdown:
                markdown = markdown.replace(url,wp_img_url[i])
    # wordpress image link re HackMD 的圖片連結
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
    note_id_list = []
    for i in range(len(data)):
        noteURL = data[i]['publishLink']
        node_id = data[i]["id"]
        urls.append(noteURL)
        note_id_list.append(node_id)
    '''
    get view mode urls
    for i in range(len(data)):
        noteURL = f"https://hackmd.io/{data[i]['id']}?view"
        urls.append(noteURL)
    '''
    return urls,note_id_list
# use HackMD API for getting content of note
def get_hackmd_content(token,note_id):
    api = API(token)
    data = api.get_note(note_id)
    return data["content"]

