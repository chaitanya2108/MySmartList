import os
from flask import Flask, redirect, render_template, request
import speech_recognition as sr
# import our OCR function
from ocr_core import ocr_core
from flask import Flask, render_template, request

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vr')
def vr():
    return render_template('vr.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      # f = open("shooping_list.txt", "a")
      # list.append(item)
      # print(list)
      # f.write(item)
      for key,value in result.items():
             f = open("shopping_list.txt", "a")
             f.truncate(0)
             list.append(value)             
             f.write(str(list))
      return render_template("result.html",result = result)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')
