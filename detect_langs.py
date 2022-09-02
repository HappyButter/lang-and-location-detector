import cv2
import numpy as np
from langdetect import detect
import locationtagger
import pytesseract

from matplotlib import pyplot as plt
from easyocr import Reader


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Carrot\AppData\Local\Tesseract-OCR\tesseract"

# DEFAULTS 
MIN_CONFIDENCE=0.5
IMG_WIDTH=320  # must be multiple of 32
IMG_HEIGHT=320 # must be multiple of 32
LAYER_NAMES = [ "feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

NORMAL_LANGS = ['en','es','it','de','fr'] # ang, hiszp, włoski, niemiecki, francuski
CHINASE_LANG = ['ch_sim','en'] # chiński uproszczony 
JAPANESE_LANG = ['ja','en'] # japoński
LANGS = [NORMAL_LANGS, CHINASE_LANG, JAPANESE_LANG] 



def detect_lang(text):
    try:
        estimated_lang = detect(text)
        
        print("Estimated lang: {}".format(estimated_lang))
        
        return estimated_lang
    
    except Exception as inst:
        print(type(inst)) 
        print(inst.args)
        print(inst) 
        
        return None


def detect_location_from_text_on_sign(text):
    try:
        place_entity = locationtagger.find_locations(text = result_text)

        return place_entity
    
    except Exception as inst:
        print(type(inst)) 
        print(inst.args)
        print(inst) 
        print("An exception while detecting location has occurred")
        
    return None 


def find_text_easyocr(image):
    result_text = ""
    
    for lang_box in LANGS:
        
        reader = Reader(lang_box, gpu=True)
        results = reader.readtext(image)
        
        for (bbox, text, prob) in results:
            result_text += text + " "

    return result_text
    

def find_text_custom_way(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
    
    result_text = ""
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        cropped = image[y:y + h, x:x + w]
        
        result_text += pytesseract.image_to_string(cropped) + " "

    return result_text


def cleanup_text(text):
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


if __name__ == "__main__": 
    for i in range(6):
            
        image = cv2.imread("images/{}.jpg".format(str(i+1)))


        # custom ocr
        print("\n\n\n")
        print("=" * 50)
        
        result_text = find_text_custom_way(image)
        estemated_lang = detect_lang(result_text)
        
        print("CUSTON OCR TEXT IS: {}".format(result_text))
        print("LANG: {}".format(estemated_lang))
        
        
        # easy ocr
        print("\n")
        print("=" * 50)
        
        image_copy = image.copy()
        
        result_text = find_text_easyocr(image_copy)
        estemated_lang = detect_lang(result_text)
        
        print("EASYOCR TEXT IS: {}".format(result_text))
        print("LANG: {}".format(estemated_lang))
        
        
        # country | region | city 
        print("\n")
        print("=" * 50)
        place_entity = detect_location_from_text_on_sign(result_text)
        
        if place_entity != None: 
                
            print("The countries in text : ")
            print(place_entity.countries)
            
            print("The states in text : ")
            print(place_entity.regions)
            
            print("The cities in text : ")
            print(place_entity.cities)
        