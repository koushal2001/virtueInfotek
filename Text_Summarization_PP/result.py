from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk 
from tkinter import filedialog

import mysql.connector
from mysql.connector import Error
import time

##from translate import Translator

from PIL import Image

from tkinter import Tk, Label, Entry, Toplevel, Canvas

from PIL import Image, ImageDraw, ImageTk, ImageFont
image = Image.open('SC.jpg')


########################################################################################    
def get(text):
    login_page = Tk()
    login_page.geometry("1300x600+30+30")
    login_page.configure(background="#fcfffc")

    def LOGIN():

        def exit():
            login_page.destroy()


        result = Text(login_page)
        result.place(x = 150,y=150,height=400, width=1000)
        result.config(font=("Times new roman", 15))
        result.configure(background="#f5fff5")
        result.configure(foreground="#0000ff")
        result.insert(INSERT,text)

        label2 = Label(login_page, text="Summarized Text")
        label2.configure(background="#ffffff")
        label2.configure(foreground="#000099")
        label2.config(font=("Times new roman", 30))
        label2.place(x = 150,y=50,height=50, width=1000)


        B1 = Button(login_page, text = "BACK", command = exit)
        B1.place(x = 1200,y = 550 ,height=40, width=80)
        B1.config(font=("Times new roman", 17))
        B1.configure(background="#f5fff5")
        B1.configure(foreground="#000099")
        login_page.mainloop()

    LOGIN()


##get('ajay ladkat')
