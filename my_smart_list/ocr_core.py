from PIL import Image
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
res = []


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    
    #Cleaning the recognized text

    cleaned_text = re.sub("[\([{}/\"“'^%*#)\]$!@&|()]","",text)  
    listRes = list(cleaned_text.split("\n"))
    while("" in listRes):
        listRes.remove("")
    
    for ele in listRes:
        i = ele.strip()
        res.append(i)
    
    while("" in res):
        res.remove("")

    with open("output.txt", "a") as f:
        print(text, file=f)


    return res


if __name__ == '_main_':
    #print(ocr_core('images/ocr_example_1.png'))
    print("Shopping list image converted to list")