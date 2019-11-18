from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

#need get and post to receive data from form
@app.route('/forms', methods=['GET', 'POST'])
#form is what is used in form.validate and format.
def form():
    form = LoginForm()
    #if the form is submitted do the indent
    if form.validate_on_submit():
        #format({defname}.{name of the field}.data)
        usanam = form.username.data
        paswod = form.password.data
        if usanam == 'kevin' and paswod=='kevin':
            return "kevin page"
        else: 
            return "Form submitted. Username is {} password is {}".format(usanam, paswod)

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()