from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1> welcum to webpag<h1><p>aaaaaa<p>'

@app.route('/yoda')
def yoda():
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()