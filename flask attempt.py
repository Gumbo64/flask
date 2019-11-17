from flask import Flask, render_template
import forms

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

@app.route('/forms', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()