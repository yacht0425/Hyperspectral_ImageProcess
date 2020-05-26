# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:44:00 2020

@author: yacht
"""

import tkinter as tk
from pyproj import Proj
import numpy as np

# Process when pusshing a button
def calc_error():
    # Estimation
    object_degN = float(textHeight1.get())
    print(object_degN)
    object_degE = float(textWeight2.get())
    print(object_degE)
    
    reference_dmmN = float(textHeight3.get())
    print(reference_dmmN)
    reference_dmmE = float(textHeight4.get())
    print(reference_dmmE)
    reference_degN = (reference_dmmN/100 - 43) * 5 / 3 + 43
    reference_degE = (reference_dmmE/100 - 141) * 5 / 3 + 141
    
    convertor = Proj(proj='utm',zone=54,ellps='GRS80')
    object_utm_X, object_utm_Y = convertor(object_degE,object_degN)
    reference_utm_X, reference_utm_Y = convertor(reference_degE,reference_degN)
    print(object_utm_X)
    error = np.sqrt(np.power(reference_utm_X - object_utm_X,2) + np.power(reference_utm_Y - object_utm_Y,2))
    # Display the result on Label 'result' 
    result = "{0} m".format(error)
    labelResult['text'] = result

# Make a window
win = tk.Tk()
win.title("Caluculate Error")
win.geometry("500x250")

# Create contents in the window
labelHeight = tk.Label(win, text='Object point Northing(deg):')
labelHeight.pack()

textHeight1 = tk.Entry(win)
textHeight1.insert(tk.END, '43.123456')
textHeight1.pack()

labelWeight = tk.Label(win, text='Object point Easting(deg)')
labelWeight.pack()

textWeight2 = tk.Entry(win)
textWeight2.insert(tk.END, '141.123456')
textWeight2.pack()

labelHeight = tk.Label(win, text='Reference point Northing(dmm):')
labelHeight.pack()

textHeight3 = tk.Entry(win)
textHeight3.insert(tk.END, '4304.12345678')
textHeight3.pack()

labelHeight = tk.Label(win, text='Reference point Easting(dmm):')
labelHeight.pack()

textHeight4 = tk.Entry(win)
textHeight4.insert(tk.END, '14120.12345678')
textHeight4.pack()

labelResult = tk.Label(win, text='---')
labelResult.pack()

calcButton = tk.Button(win, text='Calculate the error')
calcButton["command"] = calc_error
calcButton.pack()

# Work this window
win.mainloop()