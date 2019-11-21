from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask import Markup
import jinja2

import shelve
global indivtext
indivtext = []


try:
    savefile = shelve.open('savefile')
    indivtext = savefile['indivtext']
except:
    pass



global username
username = "Anon"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class commentform(FlaskForm):
    comment= StringField('comment')

@app.route('/')
def home():
    global number
    number=1
    return render_template("home.html", username=username)

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

#need get and post to receive data from form
@app.route('/forms', methods=['GET', 'POST'])
#form is what is used in form.validate and format.
def form():
    form = LoginForm()
    global username
    #if the form is submitted do the indent
    if form.validate_on_submit():
        #({form}.{name of the field}.data)
        username = form.username.data
        if username == 'kevin':
            return render_template('kevinpage.html')
        else: 
            return redirect("/", code=302)

    return render_template('form.html', form=form)
@app.route('/chatroom', methods=['GET', 'POST'])
def form1():
    form1 = commentform()
    global username
    global indivtext
    br='<br>'
    if form1.validate_on_submit():
        comment = form1.comment.data
        addable= str(username) +": "+ str(comment)
        indivtext.append(addable)
        savefile = shelve.open('savefile')
        savefile['indivtext']=indivtext
    return render_template('chatroom.html',indivtext=indivtext, form=form1, username=username)
if __name__ == '__main__':
    app.debug = True
    app.run()