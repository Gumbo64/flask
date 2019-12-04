from flask import Flask, render_template, redirect, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, AnonymousUserMixin
from datetime import datetime
import shelve
import time
import webbrowser

import jinja2

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




app = Flask(__name__)
app.config['SECRET_KEY'] = 'zbnjlbrkns'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3',connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)()
base = declarative_base()

global buildings
buildings = {}
global buildingnames
buildingnames = {}
global savefile
savefile = {}

try:
    savefile = shelve.open('savefile', writeback=True)
    buildings = savefile['buildings']
    buildingnames = savefile['buildingnames']
except:
    pass


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

class Wafertable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    wafers = db.Column(db.Integer, default = 0)
    multiplier = db.Column(db.Integer, default = 1)
    lasttime = db.Column(db.DateTime, default=datetime.now)

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class generalform(FlaskForm):
    text = StringField('text')
    text2 = StringField('text2')

def countwafers(layer, single, user_buildings):
    countingsps = 0
    if layer == None:
        for position in user_buildings:
            countingsps=countingsps + (5**position) * user_buildings[position]
    else:
        if single == True:
            countingsps = (5**layer)
        else: 
            countingsps = (5**layer) * user_buildings[layer]
    return countingsps




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
    global buildingnames
    global buildings
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data)
        db.session.add(user)
        wafer = Wafertable(username=form.username.data)
        db.session.add(wafer)
        db.session.commit()
        buildings[form.username.data]=[]
        buildingnames[form.username.data]=[]
        savefile.close()
        savefile.open()
        return redirect("/", code=302)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginform():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        try:
            user = User.query.filter_by(username=loginform.username.data).first()
            if user.check_password(user.password, loginform.password.data):
                login_user(user)
                return redirect("/", code=302)
            else:
                pass#Flask.flash('Wrong info noob')
        except:
            pass#Flask.flash('Wrong info noob')
        
    return render_template('login.html',form=loginform)

@app.route('/_chatroom', methods = ['GET'])
def chatrequest():
    totaltext = []
    query = Chatroom.query.all()
    for comment in query:
        adder = str(comment.time) + ") " + str(comment.username) + ": " + str(comment.text)
        totaltext.append(adder)
    return jsonify(totaltext=totaltext)


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if not current_user.is_authenticated:
        return "log in noob"
    form = generalform()
    if form.validate_on_submit():
        comment = form.text.data
        username = current_user.username
        if comment == r"/clear" and username == 'Rory':
            delete = Chatroom.query.all()
            for row in delete:
                db.session.delete(row)
            cleared=Chatroom(username='System',text='Chat has been cleared')
            db.session.add(cleared)
            db.session.commit()
        elif comment[0:4:1] == r"/ban" and username == 'Rory':
            ban = User.query.filter_by(username= comment[5: : ]).first()
            db.session.delete(ban)
            db.session.commit()
            cleared=Chatroom(username='System',text=ban.username + ' has been banned')
            db.session.add(cleared)
            db.session.commit()
        else:
            add = Chatroom(username=username, text=comment)
            db.session.add(add)
            db.session.commit()
    return render_template('chatroom.html',form=form, username=current_user.username)

@app.route('/_waferrequest', methods = ['GET'])
def request():
    global buildings
    user = Wafertable.query.filter_by(username=current_user.username).first()
    try:
        user_buildings = buildings[current_user.username]
    except KeyError:
        buildingnames[current_user.username] = []
        buildings[current_user.username] = []
        user_names = buildingnames[current_user.username]
        user_buildings = buildings[current_user.username]
    user.wafers = user.wafers + countwafers(None, False, user_buildings) + 1
    savefile['buildings'] = buildings
    db.session.commit()
    return jsonify(Wafers=user.wafers)

@app.route('/waferfactory', methods=['GET', 'POST'])
def waferfactory():
    global buildings
    global buildingnames
    form = generalform()
    if not current_user.is_authenticated:
        return "log in noob"
    try:
        user_names = buildingnames[current_user.username]
        user_buildings = buildings[current_user.username]
    except KeyError:
        print('got here')
        buildingnames[current_user.username] = []
        buildings[current_user.username] = [0,0]
        user_names = buildingnames[current_user.username]
        user_buildings = buildings[current_user.username]
    if form.validate_on_submit():
        try:
            layer = int(form.text.data)
            amount = int(form.text2.data)
            print(layer, amount)
            try:
                user_buildings[layer] = user_buildings[layer] + amount
                print("try1")
            except IndexError:
                user_buildings[layer] = 0
                user_buildings[layer] = user_buildings[layer] + amount
            buildings[current_user.username] = user_buildings
            #Flask.flash('Buildings bought')
            print("try2")
        except KeyError:
            print("try3")
            pass#Flask.flash('No letters!')
    print(user_buildings)
    wafertotaltext = []
    for pos in user_buildings:
        wafertotaltext.append(str(pos) + ") " + str(user_buildings[pos]) + " " + str(user_names[pos]) + " make " + str(countwafers(layer=pos, single=False, buildings=buildings)) + " per second, "+str(countwafers(layer=pos, single = True, buildings=buildings))+ " each")
    if wafertotaltext == []:
        wafertotaltext.append("No buildings yet")
    user = Wafertable.query.filter_by(username=current_user.username).first()
    return render_template("waferfactory.html", form=form, username=user.username, multiplier=user.multiplier, buildingnames = wafertotaltext)


if __name__ == '__main__':
     app.debug = True
     app.run()