from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/yoda')
def yoda():
    return render_template("yoda.html")

@app.route('/rickroll')
def new():
    return render_template("rickroll.html")


if __name__ == '__main__':
    app.debug = True
    app.run()