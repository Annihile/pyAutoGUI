from tkinter import *
from tkinter import filedialog
from tkinter import Text as textBox
from PIL import Image, ImageTk
from pytesseract import pytesseract
import os, re


path_to_tesseract = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

pytesseract.tesseract_cmd = path_to_tesseract

def selectFile():
    global filePath

    file = filedialog.askopenfile(mode='r')
    filePath = os.path.abspath(file.name)
    tesseractImgtoTxt(filePath)

def tesseractImgtoTxt(filePath):
    global img
    global textImg

    img = Image.open(filePath)
    textImg = pytesseract.image_to_string(img, lang='eng+tha')
    #print(textImg)

def filterBank():
    try:
        refID = re.search(r'\b\d{1,12}(?=.*[A-Z])[A-Z]{1,3}\d{1,5}\b', textImg)
        if refID:
            print("kasikorn")
        if not refID:
            refID = re.search(r"\d{8}(?=.*[a-zA-Z])[a-zA-Z0-9]{16,}", textImg)
            if refID:
                print("scb")
        if not refID:
            refID = re.search(r'\b\d{16}\b', textImg)
            if refID:
                print("uob")
        if not refID:
            refID = re.search(r'\b\d{25}\b', textImg)
            if refID:
                print("bangkok")
        
    except IndexError as e:
        print("wat")
    
    amount = re.search(r'\b\d{1,3}(?:,?\d{3})*\.\d{2}\b', textImg)

    if refID:
        print(refID.group())
    if amount:
        print(amount.group())

def showText():
    Label(
        mainwindow,
        text = f"File Path : {str(filePath)}"
    ).pack()
    Label(
        mainwindow,
        text = f"Text from Image :\n{textImg}"
    ).pack()
    
mainwindow = Tk()
mainwindow.title("Transaction Slip Image to Text")
mainwindow.geometry('400x720')

selectFileButton = Button(
    mainwindow,
    text = "Select File to Read Text from Image",
    command = selectFile
).pack()

showTextBtn = Button(
    mainwindow,
    text = "Show file path",
    command = showText
).pack()

filterBtn = Button(
    mainwindow,
    text = "testBtn",
    command = filterBank
).pack()

mainwindow.mainloop()