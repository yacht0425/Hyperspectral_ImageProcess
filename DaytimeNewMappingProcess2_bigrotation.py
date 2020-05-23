# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:16:08 2020

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


#Define variables
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\analysis'
directory_image = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\RGB'
directory_image_rotated = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\rotated_big_RGB'
imu = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\imu.txt' 
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\gps.txt' 
kml_file_name = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\rotated_big_RGB\\20200521_wheat_daytime_RGB.kml'
kml_name = 'wheat_daytime_big_RGB'
scanrate = 110
velocity = 0.3
width = 1.0
x_pixel = 1280
offset_distance = 2
row = 2
number = 5

#Store all HS files to refer the timestamp for extracting GPS abd IMU data
os.chdir(directory_all_HS)
path = os.getcwd()
HS_files = os.listdir(directory_all_HS)
flen = len(HS_files)
print(flen)
initial_degree = ip.FirstDirection(HS_files[0],gps) #initial degree means initial yaw using rotation
initial_yaw = ip.firstYaw(HS_files[0],imu) #This is for yaw angle from second image on
print(initial_degree)


#Read first png image
os.chdir(directory_image)
initial_image = cv2.imread('0.png')
initial_image = cv2.rotate(initial_image,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here
#Concatenate images first row 
j = 0
for k in range(flen):
    for i in range(number - 1):
        os.chdir(directory_image)
        image = cv2.imread('%s.png' %i)
        image = cv2.rotate(image,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here
        if i == 0:
            all_image = np.append(initial_image,image, axis=0)
            print(all_image.shape)
        else:
            all_image = np.append(all_image,image, axis=0)
            print(all_image.shape)
            
        j = j + 1
        print('j = %d' %j)  
        
        #Confirm line working or turning. If turning then break
        os.chdir(directory_all_HS) #Move to directory of HS files
        degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
        past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw)
        diference = abs(degree - past_degree)
        print('Degree deviation = %f' %diference)
        if diference > 10:
            print('Finish the first row')
            break
    else:
        y_pixel = len(all_image)
        print(y_pixel)
        degree = ip.BigDirection(HS_files[k],HS_files[k+5],gps)
        print(degree)
        rotated_all_image = ip.big_rotation(all_image,degree,x_pixel,y_pixel)   
            
        os.chdir(directory_image_rotated)
        cv2.imwrite('big%d.png' %k, rotated_all_image)
        continue
    break

#From second row is below
for l in range(row-1):
    
    #Eliminate turning image
    for m in range(10):
        j = j + 1
        os.chdir(directory_all_HS) #Move to directory of HS files
        initial_degree = ip.FirstDirection(HS_files[j],gps) #initial degree means initial yaw using rotation
        initial_yaw = ip.firstYaw(HS_files[j],imu) #This is for yaw angle from second image on
        degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
        past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw)
        past_past_degree = ip.Yaw(HS_files[j-2],imu,initial_degree,initial_yaw)
        print('j = %d' %j)
        print(abs(degree - past_degree))
        print(abs(past_degree - past_past_degree))
        if abs(degree - past_degree) < 5 and abs(past_degree - past_past_degree) < 5: #If angle change suttles down, then break.
            print('Go to next row!')
            break
        
    os.chdir(directory_image)
    initial_image = cv2.imread('%d.png' %j)
    initial_image = cv2.rotate(initial_image,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here

    n = j + 1       
    for i in range(n,flen):
        for i in range(number - 1):
            os.chdir(directory_image)
            image = cv2.imread('%s.png' %i+n)
            print(i+n)
            image = cv2.rotate(image,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here
            if i == 0:
                all_image = np.append(initial_image,image, axis=0)
                print(all_image.shape)
            else:
                all_image = np.append(all_image,image, axis=0)
                print(all_image.shape)
                
            j = j + 1
            print('j = %d' %j)  
            
            #Confirm line working or turning. If turning then break
            os.chdir(directory_all_HS) #Move to directory of HS files
            degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
            past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw)
            difference = abs(degree - past_degree)
            print('Degree deviation = %f' %difference)
            if difference > 10:
                print('Finish the first row')
                break
        else:
            y_pixel = len(all_image)
            print(y_pixel)
            degree = ip.BigDirection(HS_files[k],HS_files[k+5],gps)
            print(degree)
            rotated_all_image = ip.big_rotation(all_image,degree,x_pixel,y_pixel)   
                
            os.chdir(directory_image_rotated)
            cv2.imwrite('big%d.png' %k, rotated_all_image)
            
            remain = flen - j
            
            if remain < number:
                n = j
                for i in range(remain):
                    os.chdir(directory_image)
                    image = cv2.imread('%s.png' %i+n)
                    print(i+n)
                    image = cv2.rotate(image,cv2.ROTATE_180) #I don't know why but completed images are opposite so modify here
                    if i == 0:
                        all_image = np.append(initial_image,image, axis=0)
                        print(all_image.shape)
                    else:
                        all_image = np.append(all_image,image, axis=0)
                        print(all_image.shape)
                        
                    j = j + 1
                    print('j = %d' %j)  
                    
                  
                y_pixel = len(all_image)
                print(y_pixel)
                degree = ip.BigDirection(HS_files[k],HS_files[k+remain],gps)
                rotated_all_image = ip.big_rotation(all_image,degree,x_pixel,y_pixel)   
                    
                os.chdir(directory_image_rotated)
                cv2.imwrite('big%d.png' %k, rotated_all_image)
                
                print('Finish all process')
                break
            
        continue
    break

'''
with open(kml_file_name,mode='w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
    f.write('<Folder>\n')
    f.write('    <name>%s</name>\n' %kml_name) 
    f.write('    <open>1</open>\n')
    coordinate = ip.imageCoordinate_for_modify(HS_files[0],gps,offset_distance,initial_degree,scanrate,velocity) 
    imagename = '0.png'
    f.write('    <GroundOverlay>\n')
    f.write('        <name>0</name>\n')
    f.write('        <Icon>\n')
    f.write('            <href>%s</href>\n' % imagename)
    f.write('            <viewBoundScale>0.75</viewBoundScale>\n')
    f.write('        </Icon>\n')
    f.write('        <LatLonBox>\n')
    f.write('            <north>%f</north>\n' %coordinate[0])
    f.write('            <south>%f</south>\n' %coordinate[2])
    f.write('            <east>%f</east>\n' %coordinate[3])
    f.write('            <west>%f</west>\n' %coordinate[1])
    f.write('        </LatLonBox>\n')
    f.write('    </GroundOverlay>\n')        
    for i in range(flen - 1):
        t = i + 1
        yaw = ip.Yaw(HS_files[t],imu,initial_degree,initial_yaw)
        coordinate = ip.imageCoordinate_for_modify(HS_files[t],gps,offset_distance,yaw,scanrate,velocity) ###CHANGE POINT
        imagename = '%d.png' %t
        f.write('    <GroundOverlay>\n')    
        f.write('        <name>%d</name>\n' %t)
        f.write('        <Icon>\n')
        f.write('            <href>%s</href>\n' % imagename)
        f.write('            <viewBoundScale>0.75</viewBoundScale>\n')
        f.write('        </Icon>\n')
        f.write('        <LatLonBox>\n')
        f.write('            <north>%f</north>\n' %coordinate[0])
        f.write('            <south>%f</south>\n' %coordinate[2])
        f.write('            <east>%f</east>\n' %coordinate[3])
        f.write('            <west>%f</west>\n' %coordinate[1])
        f.write('        </LatLonBox>\n')
        f.write('    </GroundOverlay>\n')        
    f.write('</Folder>\n</kml>')
'''


