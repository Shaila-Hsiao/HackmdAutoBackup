from PyHackMD import API

def get_hackmd_urls(token):
    api = API(token)
    # get all notes in token
    data = api.get_note_list()
    # 先測試幾個網址
    data = data[:3]
    # get view mode urls
    urls = []
    for i in range(len(data)):
        noteURL = f"https://hackmd.io/{data[i]['id']}?view"
        urls.append(noteURL)
    return urls
