from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
global username
username = "none"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

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
        #format({defname}.{name of the field}.data)
        username = form.username.data
        paswod = form.password.data
        if username == 'kevin':
            return render_template('kevinpage.html')
        else: 
            return redirect("/", code=302)

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()