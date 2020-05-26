# -*- coding: utf-8 -*-
"""
Created on Fri May 22 08:40:51 2020

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

#Define all variables
directory_all_west = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\analysis'
directory_whiteboard = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\whiteboard'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\NDVI_800_680'
filename_white = 'white.nh7'
Lambda1 = 800 #Wavelength lamdas1
Lambda2 = 680 #Wavelength lamdas2
white_ROI_Lx = 775 #white resion: Lx < x < Rx, Uy < y < By
white_ROI_Rx = 819
white_ROI_Uy = 192
white_ROI_By = 236

#Convert lambda(nm) into number
L1 = int((Lambda1 - 350) / 5)
L2 = int((Lambda2 - 350) / 5)

#Read white data ,and extract objective wavelength from white data
white_raw = ip.readfile(directory_whiteboard,filename_white)

white_matrix_L1 = ip.white_matrix_lambda(white_raw,L1,white_ROI_Lx,white_ROI_Rx,white_ROI_Uy,white_ROI_By)
white_matrix_L2 = ip.white_matrix_lambda(white_raw,L2,white_ROI_Lx,white_ROI_Rx,white_ROI_Uy,white_ROI_By)

white_matrix_L1_mean = np.mean(white_matrix_L1) #calculate mean value
white_matrix_L2_mean = np.mean(white_matrix_L2)

white_L1_fit = np.ones((1024,1280)) * int(white_matrix_L1_mean)
white_L2_fit = np.ones((1024,1280)) * int(white_matrix_L2_mean)

#print(white_L1_fit)
#print(white_L2_fit)

#Read wheat data ,and extract objective wavelength from wheat data
HS_files = os.listdir(directory_all_west)

ftype = type(HS_files)
flen = len(HS_files)
#print("file type is %s" % ftype)
#print("file length = %s" % flen)
j = len(HS_files)

for i in range(j):
    HS_object = ip.readfile(directory_all_west,HS_files[i])
    
    HS_object_L1 = HS_object[:,L1,:]
    HS_object_L2 = HS_object[:,L2,:]
    
    #Calculate reflectance
    reflectance_object_L1 = HS_object_L1 / white_L1_fit
    reflectance_object_L2 = HS_object_L2 / white_L2_fit
    
    #Estimate NDVI
    NDVI_object = (reflectance_object_L1 - reflectance_object_L2) / (reflectance_object_L1 + reflectance_object_L2)
    
    print(NDVI_object.shape)
    norm_NDVI = cv2.normalize(NDVI_object, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    NDVI_object_color = cv2.applyColorMap(norm_NDVI, cv2.COLORMAP_WINTER) #JET,SUMMER etc.
    
    #Move to target directry and Confirm current directory
    os.chdir(directory_image)
    path = os.getcwd()
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',NDVI_object_color)
    #cv2.waitKey(0)
    cv2.imwrite('%s.png' %i, NDVI_object_color)
    #cv2.destroyAllWindows()