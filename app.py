import os, requests, json
from peewee import *
from flask import Flask
from flask import request, session, redirect, render_template, url_for
from models import *
from werkzeug import secure_filename

app = Flask(__name__)

nber = 0

@app.before_request
def before_request():
    try:
        ini_db()
    except OperationalError:
        print("connected")

@app.after_request
def after_request(response):
    db.close()
    return response

@app.route('/')
def index():
    if not session:
        return render_template('header.html') + render_template('index.html') +  render_template('footer.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    if not session:
        return render_template('header.html') + render_template('about.html') +  render_template('footer.html')
    else:
        return render_template('header.html', name=session['username']) + render_template('about.html') +  render_template('footer.html')

@app.route('/contact')
def contact():
    if not session:
        return render_template('header.html') + render_template('contact.html') +  render_template('footer.html')
    else:
        return render_template('header.html', name=session['username']) + render_template('contact.html') +  render_template('footer.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Users.select().where(Users.username == request.form['username'])
        if user.exists():
            user = Users.select().where(Users.username == request.form['username']).get()
            if request.form['username'] == user.username and request.form['password'] == user.password:
                session['username'] = user.username
                session['id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                msg = 'Wrong Username or Password, Please try again !!'
                return message(msg)
        else:
            msg = 'Username does not exist, Please try again !!'
            return message(msg)

    else:
        return redirect(url_for('index'))

@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = Users.select().where(Users.username == request.form['username'] or Users.email == request.form['email'])
        if user.exists():
            msg = 'Username/Email already exist, please try another one.'
            return message(msg)
        else:
            Users.create(
                    username = request.form['username'],
                    email = request.form['email'],
                    password = request.form['password'],
            )
        msg = 'Thank you for registering, You can now log-in '+request.form['username']+'.'
        return message(msg)
    else:
        return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    global nber
    nber = 0
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html', name=session['username']) + render_template('dashboard.html') + render_template('footer.html')

@app.route('/music')
def music():
    global nber
    nber = 0
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html', name=session['username']) + render_template('music.html') + render_template('footer.html')

@app.route("/getvideos/")
@app.route("/getvideos/<user>")
def getVideos(user=''):
    global nber
    if not session:
        return redirect(url_for('index'))
    d = Data.select()
    if(user==''):
        d = Data.select()
        if d.exists():
            d = Data.select()
    else:
        d = Data.select().where(Data.user_id == session['id'])
        if d.exists():
            d = Data.select().where(Data.user_id == session['id'])

    return conv(d)

def conv(data):
    temp = []
    for d in data:
        res = {
                'id' : d.id,
                'user_id' : d.user_id,
                'username' : d.username,
                'link' : d.link,
                'name' : d.name,
                'title' : d.title,
                'des' : d.des,
                'img' : d.img,
                'date' : d.date
        }
        temp.append(res)

    return json.dumps(temp)

@app.route('/addvideo/<vid_id>')
def addVideo(vid_id):
    link = "https://www.youtube.com/watch?v="+vid_id
    if not session:
        return redirect(url_for('index'))

    l = Data.select().where(Data.user_id == session['id'] and Data.link == link)
    if l.exists():
        msg = "This link already exists : "+ link+" ."
        response = {
            'msg': msg
        }
        return json.dumps(response)
        #return render_template('header.html', name=session['username']) + render_template('dashboard.html', msg=msg ,data=d) + render_template('footer.html')
    else:
        if(video(link, session['id'], session['username'])):
            msg = "Link has been added : "+ link+" ."
            response = {
                'msg': msg
            }
            return json.dumps(response)
        else:
            msg = "Invalid link : "+ link+" ."
            response = {
                'msg': msg
            }
            return json.dumps(response)
        #return render_template('header.html', name=session['username']) + render_template('dashboard.html', msg=msg ,data=d) + render_template('footer.html')

@app.route('/remove/<vid_id>')
def remove(vid_id):
    if not session:
        return redirect(url_for('index'))
    if len(vid_id) != 11:
        msg = "Wrong Video Id."
        response = {
                'msg': msg
            }
        return json.dumps(response)

    l = "https://www.youtube.com/watch?v="+vid_id
    c = ''
    n = ''
    if(session['username'] == 'medyas'):
        test = Data.select().where((Data.link == l))
        if test.exists():
            r = Data.select().where((Data.link == l)).execute()
            test = Data.select().where((Data.link == l)).get()
            for a in r:
                c=  a.link
                n = a.name
        else :
            msg = "This Video does not exists in your list."
            response = {
                'msg': msg
            }
            return json.dumps(response)
    else:
        test = Data.select().where((Data.link == l) & (Data.user_id == session['id']))
        if test.exists():
            r = Data.select().where((Data.link == l) & (Data.user_id == session['id'])).execute()
            test = Data.select().where((Data.link == l) & (Data.user_id == session['id'])).get()

            for a in r:
                c=  a.link
                n = a.name
        else :
            msg = "This Video does not exists in your list."
            response = {
                'msg': msg
            }
            return json.dumps(response)
    rm = "static/uploads/" + n
    test.delete_instance()
    try:
        os.remove(rm)
    except FileNotFoundError:
        print('file not found')
    msg = "Video has been deleted."
    response = {
                'msg': msg
            }
    return json.dumps(response)

@app.route('/setting', methods=['POST',  'GET'])
def setting():
    if not session:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        q = Users.select().where(Users.id == session['id']).get()
        if q.password == request.form['old'] and request.form['password'] == request.form['confirmation']:
            query = Users.update( password = request.form['password']).where(Users.id == session['id'])
            query.execute()
            msg = "Password has been changed !!"
            message(msg)
        else:
            msg = "Invalid Password/Confirmation !!!"
            message(msg)
    else:
        return render_template('header.html', name=session['username']) + render_template('setting.html') + render_template('footer.html')

@app.route('/admin', methods=['GET'])
def admin():
    if not session:
        return redirect(url_for('index'))
    if(session['username'] == 'medyas'):
        users = Users.select()
        if users.exists():
            users = Users.select()

        return render_template('header.html', name=session['username']) + render_template('admin.html', users=users) + render_template('footer.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    if not session:
        return redirect(url_for('index'))
    else:
        session.pop('username', None)
        session.pop('id', None)
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    if not session:
        return render_template('header.html') + render_template('404.html') + render_template('footer.html'), 404
    else:
        return render_template('header.html', name=session['username']) + render_template('404.html') + render_template('footer.html'), 404

app.secret_key = os.urandom(512)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 8080)), debug=True)
