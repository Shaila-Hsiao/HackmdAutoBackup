from PyHackMD import API

# get user's url of notes
def get_hackmd_urls(token):
    api = API(token)
    # get all notes in token
    data = api.get_note_list()
    # FIXME: test
    data = data[:3]
    # get url of notes
    urls = []
    for i in range(len(data)):
        noteURL = {data[i]['publishLink']}
        urls.append(noteURL)
    '''
    # get view mode urls
    for i in range(len(data)):
        noteURL = f"https://hackmd.io/{data[i]['id']}?view"
        urls.append(noteURL)
    '''
    return urls
