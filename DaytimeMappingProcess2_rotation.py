# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:08:58 2020

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
#import numpy as np
#from matplotlib import pyplot as plt


#Define variables
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\RGB'
directory_image_rotated = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\rotated_RGB'
imu = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\imu.txt' 
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\gps.txt' 
scanrate = 110
width = 1.0


#Store all HS files to refer the timestamp for extracting GPS abd IMU data
os.chdir(directory_all_HS)
path = os.getcwd()
HS_files = os.listdir(directory_all_HS)
flen = len(HS_files)
print(flen)
initial_degree = ip.FirstDirection(HS_files[0],gps) #initial degree means initial yaw using rotation
initial_yaw = ip.firstYaw(HS_files[0],imu) #This is for yaw angle from second image on
velocity = ip.speed(HS_files[0],HS_files[163],gps)
print('velocity is %f' %velocity)

#Read png image
os.chdir(directory_image)
initial = 0
ndvi = cv2.imread('%s.png' %initial)
ndvi = cv2.rotate(ndvi,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here

#Give rotation angle to the png image
os.chdir(directory_all_HS)
velocity = ip.speed(HS_files[0],HS_files[1],gps)
rotated_ndvi = ip.rotation(ndvi,initial_degree,scanrate,velocity,width)

os.chdir(directory_image_rotated)
#cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#cv2.imshow('img',rotated_ndvi)
#cv2.waitKey(0)
cv2.imwrite('0.png', rotated_ndvi)
#cv2.destroyAllWindows() 
print('0 done')

for i in range(flen - 1):
    t = i+1
    os.chdir(directory_all_HS) #Move to directory of HS files
    degree = ip.Yaw(HS_files[t],imu,initial_degree,initial_yaw)
    past_degree = ip.Yaw(HS_files[t-1],imu,initial_degree,initial_yaw)
    #print(degree)
    #print(past_degree)
    #Initialize yaw direction if the difference between past and current degree is larger than 20 
    if abs(degree - past_degree) > 10:
        initial_degree = ip.FirstDirection(HS_files[t],gps) #initial degree means initial yaw using rotation
        initial_yaw = ip.firstYaw(HS_files[t],imu) #This is for yaw angle from second image on
        degree = ip.Yaw(HS_files[t],imu,initial_degree,initial_yaw)
        print('IMU Initialized!')
    os.chdir(directory_image) #Move to directory of images
    ndvi = cv2.imread('%s.png' %t)
    rotated_ndvi = ip.rotation(ndvi,degree,scanrate,velocity,width)
    os.chdir(directory_image_rotated) #Move to directory of rotated images
    cv2.imwrite('%s.png' %t, rotated_ndvi)
    print('%d done' %t)




