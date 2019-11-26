from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from datetime import datetime
import jinja2



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    joindate = db.Column(db.DateTime, default=datetime.now)
class chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messager = db.Column(db.String(20), unique=True, nullable=False)
    text = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)



class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class commentform(FlaskForm):
    comment= StringField('comment')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("home.html", name= 'a')

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(name = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/", code=302)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginform():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        try:
            tempuser = user.query.filter_by(name=loginform.username.data)
            if loginform.password.data == User.password:
                login_user()

        except:
            return 'Wrong info'
        
        

    return render_template('login.html',form=loginform)
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    form = commentform()
    totaltext = []
    if form.validate_on_submit():
        comment = form.comment.data
        chatroom = chatroom(messager=User.name, text=comment)
        db.session.add(chatroom)
        db.session.commit()
    for comment in chatroom.query.all:
        adder = comment.time + ") " + comment.messager + ": " + comment.text
        totaltext.append(adder)
    return render_template('chatroom.html',form=form, name=User.name,chatroom = totaltext)
    
if __name__ == '__main__':
    app.debug = True
    app.run()






# #old code
# #  try:
# #     pass
# # except:
# #     form1 = commentform()
# #     global username
# #     global indivtext
# #     if form1.validate_on_submit():
# #         comment = form1.comment.data
# #         addable= str(username) +": "+ str(comment)
# #         indivtext.append(addable)
# #         savefile = shelve.open('savefile')
# #         savefile['indivtext']=indivtext
# #     return render_template('chatroom.html',indivtext=indivtext, form=form1, username=username)



# #     if username == 'kevin':
# #             return render_template('kevinpage.html')
# #     else: 
# #             return redirect("/", code=302)
 