# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:08:15 2020

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
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\RGB'
imu = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\imu.txt' 
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\gps.txt' 
row = 2
r = 650 #700nm
g = 550 #545nm
b = 450 #480nm

#Convert lambda(nm) into number
r = int((r - 350) / 5)
g = int((g - 350) / 5)
b = int((b - 350) / 5)

#Store the filename of all HS files
os.chdir(directory_all_HS)
HS_files = os.listdir(directory_all_HS)
ftype = type(HS_files)
flen = len(HS_files)

#Get gain
gain = ip.gain_RGB(directory_all_HS,HS_files[0],r,g,b)

#Get initial RGB image
initial_norm_image_RGB = ip.copy_RGB(directory_all_HS,HS_files[0],r,g,b)

j = 0
for i in range(flen):
    
    '''
    #Open image files
    os.chdir(directory_all_HS)
    f = open(HS_files[i+1],'rb') #Read binary data
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
    
    #Corresponding to the image brightness, gain is changed.
    image_RGB = image_RGB * gain
    
    norm_image_RGB = np.array(np.round(image_RGB * 16),dtype=np.uint16)  #Normalization    
    
    if i == 0:
        all_norm_image_RGB = np.append(initial_norm_image_RGB,norm_image_RGB, axis=0)
        print(all_norm_image_RGB.shape)
    else:
        all_norm_image_RGB = np.append(all_norm_image_RGB,norm_image_RGB, axis=0)
        print(norm_image_RGB.shape)
    '''
    j = j + 1
    print('j = %d' %j)  
    
    #Confirm line working or turning. If turning then break
    os.chdir(directory_all_HS) #Move to directory of HS files
    initial_degree = ip.FirstDirection(HS_files[0],gps) #initial degree means initial yaw using rotation
    initial_yaw = ip.firstYaw(HS_files[0],imu) #This is for yaw angle from second image on
    degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
    past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw)
    diference = abs(degree - past_degree)
    print('Degree deviation = %f' %diference)
    if diference > 10:
        print('Finish the first row')
        break
   
    
    

'''    
os.chdir(directory_image)
#cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#cv2.imshow('img',norm_image_RGB)
#cv2.waitKey(0)
cv2.imwrite('big0.png' , all_norm_image_RGB)
#cv2.destroyAllWindows()
'''


for l in range(row-1):
    
    for m in range(10):
        j = j + 1
        if j > flen:
            break
        os.chdir(directory_all_HS) #Move to directory of HS files
        initial_degree = ip.FirstDirection(HS_files[j],gps) #initial degree means initial yaw using rotation
        initial_yaw = ip.firstYaw(HS_files[j],imu) #This is for yaw angle from second image on
        degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
        past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw)
        past_past_degree = ip.Yaw(HS_files[j-2],imu,initial_degree,initial_yaw)
        print('j = %d' %j)
        print(abs(degree - past_degree))
        print(abs(past_degree - past_past_degree))
        if abs(degree - past_degree) < 5 and abs(past_degree - past_past_degree) < 5:
            print('Go to next row!')
            break
        
    
    initial_norm_image_RGB = ip.copy_RGB(directory_all_HS,HS_files[j],r,g,b)
    n = j        
    for i in range(n,flen):
        
        #Open image files
        os.chdir(directory_all_HS)
        f = open(HS_files[i+1],'rb') #Read binary data
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
        
        #Corresponding to the image brightness, gain is changed.
        image_RGB = image_RGB * gain
        
        norm_image_RGB = np.array(np.round(image_RGB * 16),dtype=np.uint16)  #Normalization    
    
        if i == n:
            all_norm_image_RGB = np.append(initial_norm_image_RGB,norm_image_RGB, axis=0)
            print(all_norm_image_RGB.shape)
        else:
            all_norm_image_RGB = np.append(all_norm_image_RGB,norm_image_RGB, axis=0)
            print(norm_image_RGB.shape)
    
        j = j + 1
        print('j = %d' %j)    
        if j > flen:
            break
    
    os.chdir(directory_image)
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',norm_image_RGB)
    #cv2.waitKey(0)
    cv2.imwrite('big%d.png' %l+1, all_norm_image_RGB)
    #cv2.destroyAllWindows()

    
    
