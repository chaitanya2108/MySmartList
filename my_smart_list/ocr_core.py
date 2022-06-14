from PIL import Image
import pytesseract
import re
from autocorrect import autocorrect

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    res = []
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


    final_res = autocorrect(res)

    return final_res


if __name__ == '_main_':
    #print(ocr_core('images/ocr_example_1.png'))
    print("Shopping list image converted to list")