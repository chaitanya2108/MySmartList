from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vr')
def vr():
    return render_template('vr.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')