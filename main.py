from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

with open(r'C:\Users\Kajal\Desktop\flaskpy\config.json', 'r')as c:
    params = json.load(c)['params']


app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['app-password']
)
mail = Mail(app)
local_server=True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db=SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
   
class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)

class usersignup(db.Model):
     sno = db.Column(db.Integer, primary_key=True,autoincrement=True)
     firstname = db.Column(db.String(80), nullable=False)
     lastname = db.Column(db.String(80), nullable=False)
     username = db.Column(db.String(80), nullable=False)
     password = db.Column(db.String(80), nullable=False)

@app.route("/")
def home():
    return render_template('index1.html',params=params)

@app.route("/post/", methods=['GET'])
def post_route_default():
    post = posts.query.filter_by(slug='default').first()
    return render_template('post.html', params=params, post=post)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/login", methods=['GET', 'POST'])
def login():
    
      if(request.method=='POST'):
          username=request.form.get('username')
          password=request.form.get('password')

          app.logger.info(f"User input username:{'username'}")
          app.logger.info(f"User inpuut password:{'password'}")

          userinfo=usersignup.query.filter_by(username=username).first()
        
          if userinfo.username==username  and userinfo.password==password:
              print(f"user is valid and exists")
              print(f"user found {vars(userinfo)}")

          else:
              print("user not found")

      else:
          userinfo=None           
            
      return render_template("login.html", params=params)
      
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
     if(request.method=='POST'):
        firstname  = request.form.get('first_name')
        lastname = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        entry = usersignup(firstname=firstname, lastname = lastname, username = username, password=password)
        db.session.add(entry)
        db.session.commit()

     return render_template("signup.html", params=params)    


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, phone_num = phone, message = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
       
    return render_template('contact.html',params=params)
    

app.run(debug=True)

