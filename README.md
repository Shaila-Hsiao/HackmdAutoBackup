# HackMD 備份至 Wordpress

## Concept Development
<!-- Why does your team want to build this idea/project?  -->
近期 Imgur 宣布會刪除部分照片，包括觸及率低、色情、違法的照片，因此像是我們個人的筆記可能就會因為觸及率低的原因被刪除，而 HackMD 本身是可以下載備份檔案，但只會備份文字內容(.md)，照片依舊是以 Imgur 連結的方式來顯示，因此若 Imgur 官方刪除照片時，照片就真的會完全消失了。
因此我們希望可以透過自行建立 WordPress，將 Hackmd 上的所有內容 ( 文字 & 圖片 )，完整備份至自己的 WordPress 上，同時也將 HackMD 的圖片來源改為自己 Wordpress 的連結，避免以後 HackMD 之後可能會因圖片上傳限制收錢。
## Implementation Resources

<!-- e.g., How many Raspberry Pi? How much you spent on these resources? -->
- 一台 Virtual Box (Unbuntu 20.04)
## Existing Library/Software
<!-- Which libraries do you use while you implement the project -->
- 爬蟲： Beautiful Soup
- 後端：Python Flask
- 擴充套件：Chrome Extension
- API: HackMD API
- Python 3
- Wordpress
- Database: MariaDB
- Web Sever:  Nginx 
## Implementation Process (實作流程)
<!-- What kind of problems you encounter, and how did you resolve the issue? -->
1. 取得 HackMD API Token，用 HackMD API 取得所有該 Token 所有筆記的網址
2. 利用爬蟲取得 HackMD 所有內容與圖片
3. 把 HackMD 圖片上傳到 Wordpress 上
4. 上傳成功，取得 WordPress 圖片連結，覆寫到 HackMD 共筆中





## Knowledge from Lecture

<!-- What kind of knowledge did you use on this project? -->

## Installation

<!-- How do the user install with your project? -->
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
- 安裝 openssl
	```shell=
	sudo apt-get install openssl
	```
- 下載 chromedriver
	- 查看 chrome 版本
		![](https://hackmd.io/_uploads/S1QsvbJvh.png)
		> 如果使用 ubuntu 系統可下指令 `google-chrome --version`
	- chrome 版本顯示於框框中 => 範例版本為 114
		![](https://hackmd.io/_uploads/ByeLuZyv3.png)
	- 到[ 官網下載 ](https://chromedriver.chromium.org/downloads)目前電腦 chrome 版本的 ChromeDriver （圖中為下載本範例版本示意圖）
		![](https://hackmd.io/_uploads/B1rcKW1w3.png)
- 下載 Github 專案 
	```shell=
	git clone https://github.com/Shaila-Hsiao/HackmdAutoBackup.git
	```
### 匯入 chrome extension
- 先進入 `Manage Extension` 的頁面
    </br>
	<img src="https://hackmd.io/_uploads/By0Ufp682.png" width="300x"/>
- 打開右上角 `Developer mode`
    </br>
	<img src="https://hackmd.io/_uploads/B1q6pnpU2.png" width="200x"/>
- 就會顯示 三個按鈕，點選 `Load unpacked` 上傳資料夾 `first_extension`
	<img src="https://hackmd.io/_uploads/Bk9363pUh.png" width="400x"/>
	<img src="https://hackmd.io/_uploads/By7t0h6L2.png" width="400x"/>
- 釘選擴充套件: 先點選 <img src="https://hackmd.io/_uploads/rygXl6T82.png" width="20x"/>，再點選 :pushpin:
    </br>
	<img src="https://hackmd.io/_uploads/H1HxypaIh.png" width="200x"/>
    </br>
	<img src="https://hackmd.io/_uploads/By5AReQw3.gif =200x"/>

### WordPress Server 架設 HTTPS

- 建立 Public Key、Private Key、Certificate
	- [操作流程](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8)
- 到 `/etc/nginx/sites-available` 修改 `wordpress.conf` : 新增 port 443 for SSL，並將創建好的 SSL Certificate 、Key 檔案位置放到設定檔內
	```config=
	server {
		listen 80 ;
		listen [::]:80 ;

		# SSL configuration
		listen 443 ssl ;
		listen [::]:443 ssl ;
		# SSL configuration
		root /var/www/vhost/wordpress;

		index index.php;

		server_name shaila.org;
		# Put your certificate
		ssl_certificate /home/shaila/Https/localhost.crt;
		ssl_certificate_key /home/shaila/Https/localhost.key;
		# Put your certificate
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
#### Optional : WordPress 安裝外掛 
- 此時網站不完全是 HTTPS，而是有可能變成混合內容的網站
- 到 WorPress 安裝套件 : [Really Simple SSL](https://loyseo.com/zh/how-to-change-http-in-wordpress-website-to-https/) 
	![](https://hackmd.io/_uploads/ry38inWvh.png)
	- 再到 【外掛】-> 【已安裝的外掛】-> Really Simple SSL 【啟用】 
		![](https://hackmd.io/_uploads/rJSMn2Wv3.png)
## Usage
- 開啟虛擬機 
	- 開啟 Nginx ( 確保 WordPress 正常運作 )
	- 開啟 Flask Server
	    ```cmd=
		cd ./Flask
		python3 main.py
		```
- 取得 HackMD API Token
	> 利用 Token 免登入 HackMD 就可以取得所有共筆網址
	- 創建自己的 HackMD API token
		![](https://hackmd.io/_uploads/BJkMQuoHn.png)
	- 幫自己的 token 取名字（隨便取XD）
		![](https://hackmd.io/_uploads/Bkc97djHn.png)
- 點選擴充套件，輸入 API、Wordpress 的 user、password、url，按下確認
- 就可以到 WordPress 查看 HackMD 內容
<!-- How to use your project -->
## 遇到的問題
- 權限不足問題，無法寫入 wordpress 檔案 ( 無法安裝任何套件 )
	- 修該權限 為 `www-data` 讓 wordpress 有權限更改 : 
		- `www-data` 是一個 system user，給 web servers 使用的特定 user/group。 
		- 設定某資料夾為 www-data 是希望 web servers 不要有太高的權限，同時讓 web application 適當進行寫入。 
		```shell=
		sudo chown -R www-data: /var/www/vhost/wordpress
		```
		
- 照片無法正常於 Hackmd 上讀取 : 
	- 發現 Console 報錯 : 共筆內圖片網址為 `http://....`，網頁回傳報錯顯示 `https://...`
		![](https://hackmd.io/_uploads/SykEAjWP2.png)
		- Hackmd 請求圖片資源都是由 `https://...` 去請求
		- 因此我們就將 WordPress 加上 SSL 
## 感謝名單
- 題材發想 : @PengLaiRenOu、@Huei-Lin-Lin 、squidxoxo
- 技術協助 : @Huei-Lin-Lin、秋分
## Job Assignment

## References
- [柏瑋&歐哲安 MediumToWordPress](https://github.com/NCNU-OpenSource/MediumToWordPress)
- [[筆記] 從零開始製作 Chrome 套件到上架商店](https://medium.com/%E9%BA%A5%E5%85%8B%E7%9A%84%E5%8D%8A%E8%B7%AF%E5%87%BA%E5%AE%B6%E7%AD%86%E8%A8%98/%E7%AD%86%E8%A8%98-%E5%BE%9E%E9%9B%B6%E9%96%8B%E5%A7%8B%E8%A3%BD%E4%BD%9C-chrome-%E5%A5%97%E4%BB%B6%E5%88%B0%E4%B8%8A%E6%9E%B6%E5%95%86%E5%BA%97-4971ed79ac77)
- [How to add/use chrome extension with automated Selenium browser using Python | Windows/Linux/MacOS](https://www.youtube.com/watch?v=Fx1hbZMVS7k&ab_channel=ComputingHUB)
- [Write Chrome Extensions in Python](https://medium.com/pythoniq/write-chrome-extensions-in-python-6c6b0e2e1573)
- [從 JavaScript 呼叫 Python](https://www.delftstack.com/zh-tw/howto/javascript/call-python-from-javascript/)
- [How to create an HTTPS certificate for localhost domains](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8)
