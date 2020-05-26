# -*- coding: utf-8 -*-
"""
Created on Thu May 21 07:58:34 2020

@author: yacht
"""

import os
#from osgeo import gdal
#from osgeo import ogr
#from osgeo import osr
#import pandas as pd
import cv2
import sys
sys.path.append("D:\\Vebots\\My_master_research\\HSC\\Py_analysis_lib")
import imgprocess as ip
import numpy as np
#from matplotlib import pyplot as plt 
#import matplotlib.cm as cm

#Define all variables
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\image\\RGB_non_reflectance'

r = 650 #700nm
g = 550 #545nm
b = 450 #480nm

#Convert lambda(nm) into number
r = int((r - 350) / 5)
g = int((g - 350) / 5)
b = int((b - 350) / 5)

#Get HS files
os.chdir(directory_all_HS)
HS_files = os.listdir(directory_all_HS)
ftype = type(HS_files)
flen = len(HS_files)
print('File number is %d' %flen)

#Get a gain
gain = ip.gain_RGB(directory_all_HS,HS_files[0],r,g,b)

for i in range(flen):
    #Open image files
    os.chdir(directory_all_HS)
    f = open(HS_files[i],'rb') #Read binary data
    dbuf = np.fromfile(f,dtype=np.uint16,count=-1) #Assign the format
    f.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    img_list = np.array(dlc) #Convert array to np.array
    
    img_r = img_list[:,r,:] 
    img_g = img_list[:,g,:] 
    img_b = img_list[:,b,:] 
    
    print(np.max(img_r))
    print(np.max(img_g))
    print(np.max(img_b))
    
    reimg_r = img_r.transpose(1,0) #Switch x,y axis
    reimg_g = img_g.transpose(1,0) 
    reimg_b = img_b.transpose(1,0) 
    
    image_RGB = np.concatenate([[reimg_b],[reimg_g],[reimg_r]]) #Get together r,g,b
    image_RGB = image_RGB.transpose(2,1,0)  #Switch y axis for wavelength L
    image_RGB = image_RGB * gain    
    norm_image_RGB = np.array(np.round(image_RGB * 16),dtype=np.uint16)
    
    os.chdir(directory_image)
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',norm_image_RGB)
    #cv2.waitKey(0)
    cv2.imwrite('%s.png' %i, norm_image_RGB)
    #cv2.destroyAllWindows()
