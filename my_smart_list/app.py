import os
import time
from flask import Flask, redirect, render_template, request
import speech_recognition as sr
# import our OCR function
from ocr_core import ocr_core
from flask import Flask, render_template, request
import pandas as pd
from webscraping import webscraping
# from localStoragePy import localStoragePy
from flask import session


# localStorage = localStoragePy('MySmartList', 'storage.txt')

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = "super secret key"

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
   global flag 
   flag = 0 
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

      session['vr_list'] = voice_list
      return render_template("result.html",result = result)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the upload page
@app.route('/ocr', methods=['GET', 'POST'])

def upload_page():
    global extracted_text
    global flag 
    flag  = 1
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
            session['ocr_list'] = extracted_text
            #localStorage.setItem("ocr", extracted_text)

            return render_template('upload.html',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

def list_from_user():
    return session['ocr_list'] if flag==1 else session['vr_list']
    
global actual_list 
actual_list = session['ocr_list'] if flag==1 else session['vr_list']

@app.route('/continueShopping')
def continueShopping():
    # webscraping()
    for i in actual_list:
        print("Type",type(actual_list), actual_list, i)
        iterate(i)
        actual_list.remove(i)
        

def iterate(shopping_item):
    global flag
    webscraping(shopping_item) 
    if flag==1:
        session['ocr_list'].remove(shopping_item)#remove(i)
    else:
        session['vr_list'] = session['vr_list'].remove(i)
    df = pd.read_csv('consolidated.csv')
    descriptionList = []
    priceList = []
    ratingList = []
    reviewCountList = []
    urlList = []
    imageSRCList = []
    count = len(df.index)
    for ind in df.index:
        descriptionList.append(df['Description'][ind])
        priceList.append(df['Price'][ind])
        ratingList.append(df['Rating'][ind])
        reviewCountList.append(df['ReviewCount'][ind])
        urlList.append(df['Url'][ind])
        imageSRCList.append(df['Image src'][ind])
    return render_template('continueShopping.html', descriptions=descriptionList, prices=priceList, ratings=ratingList, reviewCounts=reviewCountList, urls=urlList, imageSRCs=imageSRCList, count=count)
        
    
@app.route('/display_items')
def csvtohtml():
    global flag
    webscraping(session['ocr_list']) if flag==1 else webscraping(session['vr_list'])
    # list = ['apple']
    #webscraping(session['ocr_list'])
    df = pd.read_csv('consolidated.csv')
    return render_template('display.html', tables=[df.to_html()], titles=[''])

	
if __name__ == '__main__':
    app.debug = True
    app.run()