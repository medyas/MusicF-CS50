import urllib, json
import os
import binascii

url = urllib.urlopen("https://www.googleapis.com/youtube/v3/videos?id=2vjPBrBU-TM&key=AIzaSyCgOjKVz-KKaw8Pgt36yAUzzmdaqlHIdNg%20&part=snippet")

data = json.loads(url.read())
print data['items'][0]['snippet']['publishedAt']
#print data['items'][0]['snippet']['description']
#print data['items'][0]['snippet']['thumbnails']['default']['url']

vid = "https://www.youtube.com/watch?v=2vjPBrBU-TM"
v = ''
print len(vid)
for i in range(len(vid)-11,len(vid)):
    v+=vid[i]
print v    

secret_key = os.urandom(512)
print secret_key
print binascii.hexlify(secret_key).decode()

user = Users.select().where(Users.username == request.form['username'] or Users.email == request.form['email'])
        if user.exists():
            msg = 'Username already exist, please try another one.'            
            message(msg)
        else:
            Users.create(
                    username = request.form['username'],
                    email = request.form['email'],
                    password = request.form['password']
            )
            msg = 'Thank you for registaring, You can now log-in'            
            message(msg)
            
            
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

browser = webdriver.Firefox()
browser.get("http://www.yt-mp3.com/watch?v=cXAxpoC8o9w")
time.sleep(6)
download = browser.find_element_by_class_name('download')
ActionChains(browser).move_to_element(download).perform()
print "MP3 link is", download.get_attribute("href")