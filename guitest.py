from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import tkinter
import math
import json
import os
import time
import linecache

def grid_list(label_list):
    count = 1
    for label in label_list:
        label.grid(row=count, column=0, columnspan=2, sticky=tkinter.W)
        count += 1

def make_gui():


    gui = tkinter.Tk()
    gui.geometry("500x320")

    # create search bar
    tkinter.Button(gui, text="Search").grid(row=0, column=0, sticky=tkinter.W)
    gui_search = tkinter.Entry(gui, width=48)
    gui_search.grid(row=0, column = 1, sticky=tkinter.W)

    label_list = []
    for i in range(12):
        label_list.append(tkinter.Label(gui, text=""))
    grid_list(label_list)
    
    gui.mainloop()

make_gui()