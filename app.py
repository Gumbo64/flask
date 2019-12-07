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
    username = db.Column(db.String(20), nullable=False)
    wafers = db.Column(db.String(9999999999999999999999999999999999), nullable=False)
    multiplier = db.Column(db.Integer, default = 1)
    lasttime = db.Column(db.DateTime, default=datetime.now)

class Buildings(db.Model):
    __table_args__ = (
        db.UniqueConstraint('username', 'layer', name='nocombo'),
    )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    layer = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default = 0)
    name = db.Column(db.String(20), nullable=False, default='unnamed')

    def price(self):
        price = (5**self.layer) * (1.15**self.amount) * 10
        return price
        
        
    def indivproduce(self):
        indivproduce = (5**self.layer) * self.layer
        return indivproduce





class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class generalform(FlaskForm):
    text = StringField('text')
    text2 = StringField('text2')

def totalwafers():
    totalwafers = 0
    userbuildings = Buildings.query.filter_by(username=current_user.username).all()
    for indiv in userbuildings:
        totalwafers = totalwafers + indiv.indivproduce() * indiv.amount
    return totalwafers

def namelist():
    namelist = []
    userbuildings = Buildings.query.filter_by(username=current_user.username).all()
    for selectedlayer in userbuildings:
        add = str(selectedlayer.layer) + ") " + str(selectedlayer.amount) + " " + selectedlayer.name + " make " + str(selectedlayer.indivproduce() * selectedlayer.amount) + " per second, " + str(selectedlayer.indivproduce()) + " each. Costs " + str(selectedlayer.price())
        namelist.append(add)
    if namelist == []:
        namelist.append('No buildings yet')
    return namelist

def buy(layer, amount):

    user = Wafertable.query.filter_by(username=current_user.username).first()
    try:
        row = Buildings.query.filter_by(username=current_user.username, layer = layer).first()
        new = False
    except:
        new = True

    if layer == 0:
        autoall(user)

    else:
        if amount == 0:
            autoamount(user, layer, new)
        else:
            normalbuy(user, layer, amount, new)

def autoall(user):
    solved = True
    max = 0
    prevmax = 0
    trynew = True
    prevnew = True
    while not solved:
        try:
            row = Buildings.query.filter_by(username=current_user.username, layer = max).first()
            price = row.price()
            trynew = True
        except:
            price = (5**max) * 10
            trynew = False
        if price < int(user.wafers):
            prevmax = max
            prevnew = trynew
            max = max + 1
        else:
            layer = prevmax
            new = prevnew
            solved = False
    if layer == 0:
        #give up
        pass
    else:
        autoamount(user, layer, new)

def autoamount(user, layer, new):
    if new == True:
        price = (5**layer)* 10
    else:
        row = Buildings.query.filter_by(username=current_user.username, layer = layer).first()
        price = row.price()
    
    if int(user.wafers) < price:
        autoall(user)
    else:
        max = 1
        prevmax = 1
        while int(user.wafers) > price * max:
            prevmax = max
            max = max + 1
        amount = prevmax
        if amount == 0:
            #last resort
            autoall(user)
        else:
            #buy now
            normalbuy(user, layer, amount, new)


        

    

def normalbuy(user, layer, amount, new):
    if new == True:
        price = (5**layer)* 10
    else:
        row = Buildings.query.filter_by(username=current_user.username, layer = layer).first()
        price = row.price()

    if int(user.wafers) < price * amount:
        #can't afford normal
        autoamount(user, layer, new)
    else:
        #can afford normal
        user.wafers = str(int(user.wafers) - price * amount)
        if new == True:
            new = Buildings(username = current_user.username, layer = layer, amount = amount)
            db.session.add(new)
        else:
            row.amount = row.amount + amount
        db.session.commit()

    

        
    
def clean(wafertotaltext):
    wafertotaltext = list(dict.fromkeys(wafertotaltext))
    wafertotaltext = sorted(wafertotaltext)
    return wafertotaltext
    




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
        wafer = Wafertable(username=form.username.data, wafers = str(0))
        db.session.add(wafer)
        db.session.commit()
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
    user = Wafertable.query.filter_by(username=current_user.username).first()
    user.wafers = str(int(user.wafers) + totalwafers() + 1)
    db.session.commit()
    return jsonify(Wafers=user.wafers)

@app.route('/waferfactory', methods=['GET', 'POST'])
def waferfactory():
    wafertotaltext = []
    form = generalform()
    
    if not current_user.is_authenticated:
        return "log in noob"
    if form.validate_on_submit():
        try:
            layer = int(form.text.data)
            amount = int(form.text2.data)
            buy(layer, amount)
        except ValueError:
            pass
    user = Wafertable.query.filter_by(username=current_user.username).first()
    return render_template("waferfactory.html", form=form, username=user.username, multiplier=user.multiplier, buildingnames = namelist(), persecond = totalwafers() + 1)


if __name__ == '__main__':
     app.debug = True
     app.run()