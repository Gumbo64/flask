from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, AnonymousUserMixin
from datetime import datetime

import jinja2

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




app = Flask(__name__)
app.config['SECRET_KEY'] = 'zbnjlbrknsbjisbsnjlerjkns2io23rnferjklngijerjigwjio4ij3jnr4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3',connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)()
base = declarative_base()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    joindate = db.Column(db.DateTime, default=datetime.now)
    def check_password(self, password, checkpassword):
        if password == checkpassword:
            return True
        else:
            return False
class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class commentform(FlaskForm):
    comment = StringField('comment')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template("home.html", username='Guest')
    else:
        return render_template("home.html", username= current_user.username)

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/", code=302)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginform():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user.check_password(user.password, loginform.password.data):
            login_user(user)
            return redirect("/", code=302)
        else:
            flask.flash('Wrong info noob')
        
    return render_template('login.html',form=loginform)
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if not current_user.is_authenticated:
        return "log in noob"
    form = commentform()
    totaltext = []
    if form.validate_on_submit():
        comment = form.comment.data
        username = current_user.username
        add = Chatroom(username=username, text=comment)
        db.session.add(add)
        db.session.commit()
    query = Chatroom.query.all()
    for comment in query:
        adder = str(comment.time) + ") " + str(comment.username) + ": " + str(comment.text)
        totaltext.append(adder)
    return render_template('chatroom.html',form=form, username=current_user.username,chatroom = totaltext)
if __name__ == '__main__':
    app.debug = True
    app.run()






# #old code
# #  try:
# #     pass
# # except:
# #     form1 = commentform()
# #     global userusername
# #     global indivtext
# #     if form1.validate_on_submit():
# #         comment = form1.comment.data
# #         addable= str(userusername) +": "+ str(comment)
# #         indivtext.append(addable)
# #         savefile = shelve.open('savefile')
# #         savefile['indivtext']=indivtext
# #     return render_template('chatroom.html',indivtext=indivtext, form=form1, userusername=userusername)



# #     if userusername == 'kevin':
# #             return render_template('kevinpage.html')
# #     else: 
# #             return redirect("/", code=302)
 