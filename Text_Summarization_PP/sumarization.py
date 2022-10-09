import result
import TEXT_SUMMARIZATION
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import filedialog

import mysql.connector
from mysql.connector import Error
import time
import os
import regex


from tkinter import Tk, Label, Entry, Toplevel, Canvas

from PIL import Image, ImageDraw, ImageTk, ImageFont
image = Image.open('SC.jpg')

########################################################################################


def get():

    login_page = Tk()
    login_page.geometry("1300x600+30+30")
    login_page.configure(background="#ffffff")

    def LOGIN():

        def register():
            sumrized = TEXT_SUMMARIZATION.main()
            result.get(sumrized)

        photoimage = ImageTk.PhotoImage(image)
        Label(login_page, image=photoimage).place(x=0, y=0)

        label2 = Label(login_page, text="Text Summarization")
        label2.configure(background="#ffffFf", fg="#000066")
        label2.config(font=("Times new roman", 25))
        label2.place(x=750, y=150, height=40, width=500)

        B1 = Button(login_page, text="Upload Text File", command=register)
        B1.place(x=750, y=350, height=40, width=500)
        B1.configure(background="#f5fff5", fg="#990000")
        B1.config(font=("Times new roman", 23))

        login_page.mainloop()

    LOGIN()


get()
