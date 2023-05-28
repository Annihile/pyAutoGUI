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

def filterBank():
    try:
        refID = re.findall(r'\b\d{25}\b', textImg)          
        amount = re.findall(r'\d{1,9},\d{1,9}.00', textImg)

        print(refID[0])
        print(amount[0])
        if re.match(r'\b\d{25}\b', refID[0]):
            print("bangkok")
    except IndexError:
        pass
    
    try:
        refID = re.findall(r'\b\d{1,12}[A-Z]{1,3}\d{1,5}\b', textImg)
        amount = re.findall(r'\d{1,9},\d{1,9}.00', textImg)
        
        print(refID[0])
        print(amount[0])
        if re.match(r'\d{1,12}[A-Z]{1,3}\d{1,5}', refID[0]):
            print("kasikorn")
    except IndexError:
        pass

    try:
        refID = re.findall(r'\b\d{16}\b', textImg)
        amount = re.findall(r'\d{1,9},\d{1,9}.00', textImg)
        
        print(refID[0])
        print(amount[0])
        if re.match(r'\b\d{16}\b', refID[0]):
            print("uob")
    except IndexError:
        pass

    try:
        refID = re.findall(r"\d{8}(?=.*[a-zA-Z])[a-zA-Z0-9]{16,}", textImg)
        amount = re.findall(r'\d{1,9},\d{1,9}.00', textImg)

        print(refID[0])
        print(amount[0])
        if re.match(r"\d{8}(?=.*[a-zA-Z])[a-zA-Z0-9]{16,}", refID[0]):
            print("scb")
    except:
        pass

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