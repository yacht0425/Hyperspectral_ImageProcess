# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:52:46 2020

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
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200519wheat_nighttime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200519wheat_nighttime\\image\\RGB_pure_650_550_450'

Lambda_r = 650 #Wavelength lamdas1 #700 #650
Lambda_g = 550 #Wavelength lamdas2 #545 #550
Lambda_b = 450 #Wavelength lamdas3 #480 #450
directory_broomscanned_whitepaper = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200513tokujitsu\\After_height_changed'
filename_broomscanned_whitepaper = 'PB(s30,g100,33.31ms,350-1100)20200513_142148.nh7'
directory_whiteboard_ref = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200513tokujitsu\\Before_height_changed'
directory_whitepaper_ref = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200513tokujitsu\\Before_height_changed'
filename_whiteboard_ref = 'Img-d(s30,g70,33.31ms,350-1100)_20200513_135531.nh7'
filename_whitepaper_ref = 'Img-d(s30,g70,33.31ms,350-1100)_20200513_135948.nh7'
whiteboard_ROI_Lx = 624 #Expensive standard whiteboard resion: Lx < x < Rx, Uy < y < By
whiteboard_ROI_Rx = 679 
whiteboard_ROI_Uy = 470
whiteboard_ROI_By = 521
whitepaper_ROI_Lx = 612 #Mere white paper: Lx < x < Rx, Uy < y < By
whitepaper_ROI_Rx = 690
whitepaper_ROI_Uy = 463
whitepaper_ROI_By = 548

#Convert lambda(nm) into number
Lr = int((Lambda_r - 350) / 5)
Lg = int((Lambda_g - 350) / 5)
Lb = int((Lambda_b - 350) / 5)

#Read whiteboard and whitepaper data for calculating reflectance of whitepaper: R|paper
whiteboard_ref_raw = ip.readfile(directory_whiteboard_ref,filename_whiteboard_ref)
whitepaper_ref_raw = ip.readfile(directory_whitepaper_ref,filename_whitepaper_ref)

whiteboard_matrix_Lr = ip.white_matrix_lambda(whiteboard_ref_raw,Lr,whiteboard_ROI_Lx,whiteboard_ROI_Rx,whiteboard_ROI_Uy,whiteboard_ROI_By) #Extract ROI into a matrix
whiteboard_matrix_Lg = ip.white_matrix_lambda(whiteboard_ref_raw,Lg,whiteboard_ROI_Lx,whiteboard_ROI_Rx,whiteboard_ROI_Uy,whiteboard_ROI_By)
whiteboard_matrix_Lb = ip.white_matrix_lambda(whiteboard_ref_raw,Lb,whiteboard_ROI_Lx,whiteboard_ROI_Rx,whiteboard_ROI_Uy,whiteboard_ROI_By)
whitepaper_matrix_Lr = ip.white_matrix_lambda(whitepaper_ref_raw,Lr,whitepaper_ROI_Lx,whitepaper_ROI_Rx,whitepaper_ROI_Uy,whitepaper_ROI_By)
whitepaper_matrix_Lg = ip.white_matrix_lambda(whitepaper_ref_raw,Lg,whitepaper_ROI_Lx,whitepaper_ROI_Rx,whitepaper_ROI_Uy,whitepaper_ROI_By)
whitepaper_matrix_Lb = ip.white_matrix_lambda(whitepaper_ref_raw,Lb,whitepaper_ROI_Lx,whitepaper_ROI_Rx,whitepaper_ROI_Uy,whitepaper_ROI_By)

whiteboard_matrix_Lr_mean = np.mean(whiteboard_matrix_Lr) #calculate mean value of above matrix
whiteboard_matrix_Lg_mean = np.mean(whiteboard_matrix_Lg)
whiteboard_matrix_Lb_mean = np.mean(whiteboard_matrix_Lb)
whitepaper_matrix_Lr_mean = np.mean(whitepaper_matrix_Lr) 
whitepaper_matrix_Lg_mean = np.mean(whitepaper_matrix_Lg)
whitepaper_matrix_Lb_mean = np.mean(whitepaper_matrix_Lb)

Reflectance_whitepaper_Lr = whitepaper_matrix_Lr_mean / whiteboard_matrix_Lr_mean #This is the reflectance R|paper of Lr
Reflectance_whitepaper_Lg = whitepaper_matrix_Lg_mean / whiteboard_matrix_Lg_mean 
Reflectance_whitepaper_Lb = whitepaper_matrix_Lb_mean / whiteboard_matrix_Lb_mean 

print(Reflectance_whitepaper_Lr)
print(Reflectance_whitepaper_Lg)
print(Reflectance_whitepaper_Lb)

#Read broomscanned white paper data for light deviation correction
broomscanned_white_raw = ip.readfile(directory_broomscanned_whitepaper,filename_broomscanned_whitepaper)
broomscanned_white_Lr = broomscanned_white_raw[:,Lr,:]
broomscanned_white_Lg = broomscanned_white_raw[:,Lg,:]
broomscanned_white_Lb = broomscanned_white_raw[:,Lb,:]

broomscanned_white_Lr_filtered = cv2.blur(broomscanned_white_Lr,(20,20)) #Smoothing filter
broomscanned_white_Lg_filtered = cv2.blur(broomscanned_white_Lg,(20,20))
broomscanned_white_Lb_filtered = cv2.blur(broomscanned_white_Lb,(20,20))

#Read wheat data ,and extract objective wavelength from wheat data
HS_files = os.listdir(directory_all_HS)
ftype = type(HS_files)
flen = len(HS_files)
#print("file type is %s" % ftype)
#print("file length = %s" % flen)

for i in range(flen):
    HS_object = ip.readfile(directory_all_HS,HS_files[i])
    
    HS_object_r = HS_object[:,Lr,:]
    HS_object_g = HS_object[:,Lg,:]
    HS_object_b = HS_object[:,Lb,:]
    
    #Calculate reflectance
    reflectance_object_r = HS_object_r / broomscanned_white_Lr_filtered * Reflectance_whitepaper_Lr
    reflectance_object_g = HS_object_g / broomscanned_white_Lg_filtered * Reflectance_whitepaper_Lg
    reflectance_object_b = HS_object_r / broomscanned_white_Lb_filtered * Reflectance_whitepaper_Lb
    
    #Integrate R,G,B
    reimg_r = reflectance_object_r.transpose(1,0) #Switch x,y axis
    reimg_g = reflectance_object_g.transpose(1,0) *1.3
    reimg_b = reflectance_object_b.transpose(1,0) *0.2

    RGB_object = np.concatenate([[reimg_b],[reimg_g],[reimg_r]])
    RGB_object = RGB_object.transpose(2,1,0)
    brightness = 1.8
    norm_RGB_object = np.round(RGB_object*255*brightness)
    
    #Move to target directry and Confirm current directory
    os.chdir(directory_image)
    path = os.getcwd()
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',RGB_object)
    #cv2.waitKey(0)
    cv2.imwrite('%s.png' %i, norm_RGB_object)
    #cv2.destroyAllWindows()
    print('%d done' %i )
    


