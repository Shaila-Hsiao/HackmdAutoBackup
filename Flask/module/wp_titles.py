import xmlrpc.client

def get_wp_titles(account,wp_password,wp_url):
    # WordPress 登入資訊
    username = account
    password = wp_password
    # WordPress 網站的 URL 和 XML-RPC API 端點
    url = 'http://'+wp_url+'/xmlrpc.php'

    # 連接到 WordPress API
    wp = xmlrpc.client.ServerProxy(url)

    # 獲取文章列表
    posts = wp.metaWeblog.getRecentPosts(10000, username, password)

    wp_titles = []
    # 遍歷文章列表，獲取標題
    for post in posts:
        title = post['title']
        wp_titles.append(title)
    return wp_titles
