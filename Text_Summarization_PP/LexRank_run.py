from LexRank import summarize_by_LexRank


from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk 
from tkinter import filedialog


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()




print(' ')
print('_______________________________________________________________________')
print(' ')

f = open(file_path, encoding="utf-8")
example_sentence = f.read()
print("Input_Text : ",example_sentence)
f.close()

print('_______________________________________________________________________')
print(' ')

summarized_Text = summarize_by_LexRank.summarize(example_sentence)  

print("summarized_Text : ", summarized_Text) 
