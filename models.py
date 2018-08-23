from peewee import *
from flask import render_template
import urllib.request, json
import requests
from download import *

db = SqliteDatabase('users.db')
db2 = SqliteDatabase('data.db')


class Users(Model):
    id = PrimaryKeyField()
    email = CharField(unique = True)
    username = CharField(unique = True)
    password = CharField()

    class Meta:
        database = db

class Data(Model):
    id = PrimaryKeyField()
    user_id = IntegerField()
    username = CharField()
    link = CharField()
    name = CharField()
    title = CharField()
    des = CharField()
    img = CharField()
    date = DateTimeField()

    class Meta:
        database = db2

def ini_db():
    db.connect()
    db.create_tables([Users, Data], safe=True)

def message(msg):
    return render_template('header.html') + render_template('msg.html', msg=msg) + render_template('footer.html')

def video(vid, u_id, user):
    v = ''
    for i in range(len(vid)-11,len(vid)):
        v+=vid[i]

    r = requests.get("https://www.googleapis.com/youtube/v3/videos?id="+v+"&key=AIzaSyCO5gkG1UxAUqxEE_ElkqHJ5vxpdZ5l8yc%20&part=snippet")
    if(r.status_code == 200):
        data = r.json()
        n = parse(v, data['items'][0]['snippet']['title'])
        Data.create(
                    user_id = u_id,
                    username = user,
                    link = vid,
                    name = n,
                    title = data['items'][0]['snippet']['title'],
                    des = data['items'][0]['snippet']['description'],
                    img = data['items'][0]['snippet']['thumbnails']['medium']['url'],
                    date = data['items'][0]['snippet']['publishedAt']
                    )
        return True
    else:
        return False

