import os
import time
from flask import Flask, redirect, render_template, request
import speech_recognition as sr
# import our OCR function
from ocr_core import ocr_core
from flask import Flask, render_template, request
import pandas as pd
from webscraping import webscraping

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

voice_list = []
extracted_text =[]

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
             voice_list.append(value)             
             f.write(str(voice_list))

      return render_template("result.html",result = result)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/ocr', methods=['GET', 'POST'])

def upload_page():
    global extracted_text
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
    
            #extract the text and display it
        
            return render_template('upload.html',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/display_items')
def csvtohtml():
    # list = ['apple']
    #webscraping(extracted_text)
    df = pd.read_csv('consolidated.csv')
    return render_template('display.html', tables=[df.to_html()], titles=[''])

	
if __name__ == '__main__':
    app.debug = True
    app.run()