# lang-and-location-detector

### Setup

> NOTE: Create a Python 3.8 (or higher) virtual environment 

> NOTE: Ensure that you have opencv-python and NOT opencv-contrib-python installed in your virtual environment

1.  pip install opencv-python
2.  pip install numpy
3.  pip install torch 
4.  pip install torchvision 
5.  pip install langdetect
6.  python -m spacy download en_core_web_sm
7.  python download_packages.py
8.  Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
9.  Install this exe in 'C:/Users/YOUR_FANCY_WINDOWS_USER_NAME/AppData/Local/Programs/Tesseract-OCR'
10. pip install pytesseract 
11. In the line 11 of detect_langs.py set: pytesseract.pytesseract.tesseract_cmd = r"C:\Users\YOUR_FANCY_WINDOWS_USER_NAME\AppData\Local\Tesseract-OCR\tesseract" 

### Run

1. python detect_langs.py

### Have fun :) 
