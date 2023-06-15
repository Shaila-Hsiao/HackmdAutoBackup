# 嘿!MD 你還在窩被子裡

## Concept Development
<!-- Why does your team want to build this idea/project?  -->
近期 Imgur 宣布會刪除部分照片，包括觸及率低、色情、違法的照片，因此像是我們個人的筆記可能就會因為觸及率低的原因被刪除，而 HackMD 本身是可以下載備份檔案，但只會備份文字內容(.md)，照片依舊是以 Imgur 連結的方式來顯示，因此若 Imgur 官方刪除照片時，照片就真的會完全消失了。
因此我們希望可以透過自行建立 WordPress，將 Hackmd 上的所有內容 ( 文字 & 圖片 )，完整備份至自己的 WordPress 上，同時也將 HackMD 的圖片來源改為自己 Wordpress 的連結，避免以後 HackMD 之後可能會因圖片上傳限制收錢。
## Implementation Resources

<!-- e.g., How many Raspberry Pi? How much you spent on these resources? -->
- 一台 Virtual Box (Linux Ubuntu 20.04)
## Existing Library/Software
<!-- Which libraries do you use while you implement the project -->
- 前端框架：Bootstrap 5.0
- 擴充套件：Chrome Extension 
- 爬蟲：request 涵式庫、Beautiful Soup
- 後端：Python Flask (Python3)
- API: 
	- [HackMD API](https://hackmd.io/@hackmd-api/developer-portal/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2Fuser-notes-api)
	- [Wordpress API : XML-RPC](https://python-wordpress-xmlrpc.readthedocs.io/en/latest/ref/methods.html#wordpress_xmlrpc.methods.media.GetMediaLibrary)
- Wordpress (版本 6.2.2)
- PHP (版本 7.4)
- Database: MariaDB ( 版本 10.3.38 )
- Web Sever:  Nginx ( 版本 1.18.0)
## Implementation Process (實作流程)
<!-- What kind of problems you encounter, and how did you resolve the issue? -->
1. 取得 HackMD API Token，用 HackMD API 取得所有該 Token 所有筆記的網址
2. 利用爬蟲（權限 = 公開）或 HackMD API(權限 = 私人或登入) 取得 HackMD 所有內容與圖片
4. 把 HackMD 內容與圖片上傳到 Wordpress 上，同時檢查 HackMD 是否有重複的圖片在 WordPress，若有重複只更新異動的內容 
6. 圖片上傳成功，取得 WordPress 圖片連結，覆寫到 HackMD 共筆中
7. 上傳最新的 HackMD 共筆內容到 Wordpress，並做增量備份

## Installation
- 更新 apt
	```shell=
	sudo apt update 
	sudo apt upgrade 
	```
- 安裝 python3 套件
	```shell=
    sudo apt install python3-pip
    pip install python-wordpress-xmlrpc
    pip install Flask-Cors
    pip install selenium
    pip install python-HackMD
    pip install beautifulsoup4
	```
- 安裝 WordPress
	- [操作流程參考資料](https://hackmd.io/@pinping/wordpress教學)
	- 還需安裝的 php 套件
		```shell=
		sudo apt install php7.4-fpm php7.4-mysql php-curl php-dom php-imagick php-mbstring php-zip php-gd php-intl
		```
		> 注意安裝版本 : 此範例為 Ubuntu 20.04 安裝 php7.4
- 下載 Github 專案 
	```shell=
	git clone https://github.com/Shaila-Hsiao/HackmdAutoBackup.git
	```
### 匯入 chrome extension
- 先進入 `Manage Extension` 的頁面
	<img src="https://hackmd.io/_uploads/By0Ufp682.png" width="300x">
- 打開右上角 `Developer mode`
	<img src="https://hackmd.io/_uploads/B1q6pnpU2.png" width="200x">
- 就會顯示 三個按鈕，點選 `Load unpacked` 上傳資料夾 `first_extension`
	<img src="https://hackmd.io/_uploads/Bk9363pUh.png" width="400x">
	<img src="https://hackmd.io/_uploads/By7t0h6L2.png" width="400x">
- 釘選擴充套件: 先點選 <img src="https://hackmd.io/_uploads/rygXl6T82.png" width="20x">，再點選 :pushpin:
	<img src="https://hackmd.io/_uploads/H1HxypaIh.png" width="200x">
	<img src="https://hackmd.io/_uploads/By5AReQw3.gif" width="200x">

### WordPress Server 架設 HTTPS
- 安裝 openssl
	```shell=
	sudo apt-get install openssl
	```
- 建立 Public Key、Private Key、Certificate
	- [操作流程](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8)
- 到 `/etc/nginx/site-available` 修改 `wordpress.conf` : 新增 port 443 for SSL，並將創建好的 SSL Certificate 、Key 檔案位置放到設定檔內
	```config=
	server {
		listen 80 ;
		listen [::]:80 ;

		# SSL configuration
		listen 443 ssl ;
		listen [::]:443 ssl ;

		root /var/www/vhost/wordpress;

		index index.php;
            # FIXME:  Put your domain name
		server_name shaila.org;
		# FIXME: Put your certificate
		ssl_certificate /home/shaila/Https/localhost.crt;
		ssl_certificate_key /home/shaila/Https/localhost.key;

		location / {
			try_files $uri $uri/ =404;
		}
		location ~ \.php$ {
			include snippets/fastcgi-php.conf;
			fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
	   }

	   location /wp-photos/ {
		   alias /var/www/vhost/wordpress/wp-content/uploads/;
		}
	}

	```
- 重新啟動 Nginx
    ```terminal=
    sudo service nginx reload
    ```
#### Optional : WordPress 安裝外掛 
- 此時網站不完全是 HTTPS，而是有可能變成混合內容的網站
	> 同一網站中同時存在加密的 HTTPS 內容和非加密的 HTTP 內容，這可能會導致瀏覽器顯示安全警告或封鎖非加密的內容。
- 到 WorPress 安裝套件 : [Really Simple SSL](https://loyseo.com/zh/how-to-change-http-in-wordpress-website-to-https/) 
	<img src="https://hackmd.io/_uploads/ry38inWvh.png">
	- 再到 【外掛】-> 【已安裝的外掛】-> Really Simple SSL 【啟用】 
		<img src="https://hackmd.io/_uploads/rJSMn2Wv3.png">
## Usage
- 開啟虛擬機 
	- 開啟 Nginx
        ```cmd=
        sudo service nginx start
        ```
    - 查看 Nginx 狀態確保 WordPress 正常運作
    <img src="https://hackmd.io/_uploads/ryCjKNuDh.png">
	- 開啟 Flask Server
	    ```cmd=
		cd ./Flask
		python3 main.py
		```
- 取得 HackMD API Token
	> 利用 Token 免登入 HackMD 就可以取得所有共筆網址或是獲取私人筆記內容
	- 創建自己的 HackMD API token
		<img src="https://hackmd.io/_uploads/BJkMQuoHn.png">
	- 幫自己的 token 取名字（隨便取XD）
		<img src="https://hackmd.io/_uploads/Bkc97djHn.png">
- 點選擴充套件，輸入 API 與 Wordpress 的 Account、Password、Domain name，點選確認
	<img src="https://hackmd.io/_uploads/BkpPPKPP3.png">
- 顯示成功備份
	<img src="https://hackmd.io/_uploads/HJUXuYDDh.png">
- 就可以到 WordPress 查看已備份的 HackMD 內容
    <img src="https://hackmd.io/_uploads/SkcOsEOw2.png">
- HackMD 筆記內的圖片連結也會換成 WordPress 圖片連結

## 遇到的問題
- 權限不足問題，無法新增修改檔案寫入 wordpress 檔案 
	- 修該權限 為 `www-data` 讓 wordpress 有權限更改 : 
		- `www-data` 是一個 system user，給 web servers 使用的特定 user/group。 
		- 設定某資料夾為 www-data 是希望 web servers 不要有太高的權限，同時讓 web application 適當進行寫入。 
		```shell=
		sudo chown -R www-data: /var/www/vhost/wordpress
		```
- 照片無法正常於 Hackmd 上讀取 : 
	- 發現 Console 報錯 : 共筆內圖片網址為 `http://....`，網頁回傳報錯顯示 `https://...`
		<img src="https://hackmd.io/_uploads/SykEAjWP2.png">
		- Hackmd 請求圖片資源都是由 `https://...` 去請求
		- 因此設定 Nginx SSL ( 設定 port 443 與創建憑證 ) 
- 使用 Certbot 創建憑證 : 但沒有公開 IP 無法向 CA 申請憑證
	- 改使用 OpenSSL 建立開發測試用途的自簽憑證 (**Self-Signed Certificate**)
## 感謝名單
- 題材發想 : [@PengLaiRenOu](https://github.com/PengLaiRenOu)、[@Huei-Lin-Lin](https://github.com/Huei-Lin-Lin) 、[@squidxoxo](https://github.com/squidxoxo)
- 技術協助 : [@Huei-Lin-Lin](https://github.com/Huei-Lin-Lin)、[@秋分](https://github.com/chofinn)、[@bluet](https://github.com/bluet)
## Job Assignment
- 蕭鈺宸 : 擴充套件、Wordpress、撰寫文件
- 陳琪樺 : 爬蟲、HackMD API 串接
## References
- [柏瑋&歐哲安 MediumToWordPress](https://github.com/NCNU-OpenSource/MediumToWordPress)
- [[筆記] 從零開始製作 Chrome 套件到上架商店](https://medium.com/%E9%BA%A5%E5%85%8B%E7%9A%84%E5%8D%8A%E8%B7%AF%E5%87%BA%E5%AE%B6%E7%AD%86%E8%A8%98/%E7%AD%86%E8%A8%98-%E5%BE%9E%E9%9B%B6%E9%96%8B%E5%A7%8B%E8%A3%BD%E4%BD%9C-chrome-%E5%A5%97%E4%BB%B6%E5%88%B0%E4%B8%8A%E6%9E%B6%E5%95%86%E5%BA%97-4971ed79ac77)
- [How to add/use chrome extension with automated Selenium browser using Python | Windows/Linux/MacOS](https://www.youtube.com/watch?v=Fx1hbZMVS7k&ab_channel=ComputingHUB)
- [Write Chrome Extensions in Python](https://medium.com/pythoniq/write-chrome-extensions-in-python-6c6b0e2e1573)
- [從 JavaScript 呼叫 Python](https://www.delftstack.com/zh-tw/howto/javascript/call-python-from-javascript/)
- [How to create an HTTPS certificate for localhost domains](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8)
- [HackMD API](https://hackmd.io/@hackmd-api/developer-portal/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2Fuser-notes-api)
- [Wordpress API : XML-RPC](https://python-wordpress-xmlrpc.readthedocs.io/en/latest/ref/methods.html#wordpress_xmlrpc.methods.media.GetMediaLibrary)
- [connect to wordpress](https://github.com/whuhan2013/pythoncode/blob/master/wordpress/wordpress.py)