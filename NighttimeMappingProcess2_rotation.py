# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:14:42 2020

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
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\image\\RGB_non_reflectance'
directory_image_rotated = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\image\\rotated_RGB_non_reflectance'
imu = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\raw\\imu.txt' 
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\raw\\gps.txt' 
scanrate = 35
width = 1.4
row = 2

#Store all HS files to refer the timestamp for extracting GPS abd IMU data
os.chdir(directory_all_HS)
path = os.getcwd()
HS_files = os.listdir(directory_all_HS)
flen = len(HS_files)
print(flen)
initial_degree = ip.FirstDirection(HS_files[0],gps) #initial degree means initial yaw using rotation
initial_yaw = ip.firstYaw(HS_files[0],imu) #This is for yaw angle from second image on
velocity = ip.speed(HS_files[0],HS_files[flen//row],gps)
print('velocity is %f' %velocity)

#Read png image
os.chdir(directory_image)
initial = 0
ndvi = cv2.imread('%s.png' %initial)
ndvi = cv2.rotate(ndvi,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here

#Give rotation angle to the png image
rotated_ndvi = ip.rotation(ndvi,initial_degree,scanrate,velocity,width)

os.chdir(directory_image_rotated)
#cv2.namedWindow('img', cv2.WINDOW_NORMAL)
#cv2.imshow('img',rotated_ndvi)
#cv2.waitKey(0)
cv2.imwrite('0.png', rotated_ndvi)
#cv2.destroyAllWindows() 

for i in range(flen - 1):
    t = i+1
    os.chdir(directory_all_HS) #Move to directory of HS files
    degree = ip.Yaw(HS_files[t],imu,initial_degree,initial_yaw)
    os.chdir(directory_image) #Move to directory of images
    ndvi = cv2.imread('%s.png' %t)
    rotated_ndvi = ip.rotation(ndvi,degree,scanrate,velocity,width)
    os.chdir(directory_image_rotated) #Move to directory of rotated images
    cv2.imwrite('%s.png' %t, rotated_ndvi)
    print('%d done' %t)

