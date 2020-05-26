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
print('file number is %d' %flen)
initial_degree = ip.FirstDirection(HS_files[0],gps) #initial degree means initial yaw using rotation
initial_yaw = ip.firstYaw(HS_files[0],imu) #This is for yaw angle from second image on
print('Initial degree is %f' %initial_degree)


#Concatenate images first row 
j = 0
j_list = []
for k in range(flen):
    #Read first image
    os.chdir(directory_image)
    initial_image = cv2.imread('%d.png' %j)
    print('Next initial image is %d' %j)
    
    #concatenate images as the number of images 
    for i in range(number - 1):
        os.chdir(directory_image)
        j = j + 1
        print('j = %d' %j)
        
        image = cv2.imread('%s.png' %j)
        if i == 0: #The first append is initial and next image, the second one is all_images and next image
            all_images = np.append(initial_image,image, axis=0)
            print(all_images.shape)
        else:
            all_images = np.append(all_images,image, axis=0)
            print(all_images.shape)
        
        #Confirm line working or turning. If turning, then check the number by the end and concatenate the number of images
        os.chdir(directory_all_HS)
        degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
        next_degree = ip.Yaw(HS_files[j+number-1],imu,initial_degree,initial_yaw) #next_degree means the last image in concatenated images 
        difference = abs(degree - next_degree)
        print('Degree deviation = %f' %difference)
        #The process of the end of the row 
        if difference > 10:
            del all_images
            last_number = j
            os.chdir(directory_image)
            initial_image = cv2.imread('%d.png' %j)
            print('Last initial image is %d' %j)
            #Detect the number of remain images 
            while True:
                os.chdir(directory_all_HS) #Move to directory of HS files
                degree = ip.Yaw(HS_files[last_number],imu,initial_degree,initial_yaw)
                next_degree = ip.Yaw(HS_files[last_number+1],imu,initial_degree,initial_yaw)
                difference = abs(degree - next_degree)
                if difference < 5:
                    print('It is fine.')
                else:
                    print('Change point is detected')
                    break
                last_number = last_number + 1
            a = last_number - j
            for i in range(a):
                os.chdir(directory_image)
                j = j + 1
                print('j = %d' %j) 
                image = cv2.imread('%s.png' %j)
                if i == 0:
                    all_images = np.append(initial_image,image, axis=0)
                    print(all_images.shape)
                else:
                    all_images = np.append(all_images,image, axis=0)
                    print(all_images.shape)
                
                
            '''
            all_images = cv2.rotate(all_images,cv2.ROTATE_180)
            y_pixel = len(all_images)
            print(y_pixel)
            os.chdir(directory_all_HS)
            degree = ip.BigDirection(HS_files[j-a],HS_files[j],gps)
            print(degree)
            print(j-a)
            print(j)
            '''
            j_list.append(j)
            '''
            rotated_all_images = ip.big_rotation(all_images,degree,x_pixel,y_pixel_for_last)   
                
            os.chdir(directory_image_rotated)
            cv2.imwrite('big%d.png' %k, rotated_all_images)
            '''
            
            del all_images    
            
            print('Finish the first row')
            break
    else:
        '''
        all_images = cv2.rotate(all_images,cv2.ROTATE_180) 
        y_pixel = len(all_images)
        '''
        y_pixel_for_last = len(all_images)
        '''
        print(y_pixel)
        
        degree = ip.BigDirection(HS_files[j-4],HS_files[j],gps)
        print(degree)
        print(j-4)
        print(j)
        '''
        j_list.append(j)
        '''
        rotated_all_images = ip.big_rotation(all_images,degree,x_pixel,y_pixel)   
            
        os.chdir(directory_image_rotated)
        cv2.imwrite('big%d.png' %k, rotated_all_images)
        print('big%d.png done' %k)
        '''
        del all_images
        
        j = j + 1
        
        
        continue
    break

#From second row is below
for l in range(row-1):
    
    #Eliminate turning image
    n = j
    t = 0
    for m in range(10):
        n = n + 1
        t = t + 1
        os.chdir(directory_all_HS) #Move to directory of HS files
        initial_degree = ip.FirstDirection(HS_files[n],gps) #initial degree means initial yaw using rotation
        initial_yaw = ip.firstYaw(HS_files[n],imu) #This is for yaw angle from second image on
        degree = ip.Yaw(HS_files[n],imu,initial_degree,initial_yaw)
        next_degree = ip.Yaw(HS_files[n+1],imu,initial_degree,initial_yaw)
        next_next_degree = ip.Yaw(HS_files[n+2],imu,initial_degree,initial_yaw)
        print('j = %d' %j)
        print(abs(degree - next_degree))
        print(abs(next_degree - next_next_degree))
        if abs(degree - next_degree) < 5 and abs(next_degree - next_next_degree) < 5: #If angle change suttles down, then break.
            print('Go to next row!')
            break
        
        
    #Concatenate next row images
    j = j + t
    for u in range(flen):
        k = k + 1 #This is the number of image: k.png
        print('%d th png is making' %k)
        os.chdir(directory_image)
        print('Next initial image is %d' %j)
        initial_image = cv2.imread('%d.png' %j)
        for i in range(number - 1):
            j = j + 1
            print('j = %d' %j)
            os.chdir(directory_image)
            image = cv2.imread('%d.png' %j)
            if i == 0:
                all_images = np.append(initial_image,image, axis=0)
                print(all_images.shape)
            else:
                all_images = np.append(all_images,image, axis=0)
                print(all_images.shape)
            
            #Confirm line working or turning. If turning then break after concatenating remain images
            os.chdir(directory_all_HS) #Move to directory of HS files
            degree = ip.Yaw(HS_files[j],imu,initial_degree,initial_yaw)
            past_degree = ip.Yaw(HS_files[j-1],imu,initial_degree,initial_yaw) #next_degree means the last image in concatenated images 
            difference = abs(degree - past_degree)
            print('Degree deviation = %f' %difference)
            if difference > 10:
                del all_images
                last_number = j
                os.chdir(directory_image)
                initial_image = cv2.imread('%d.png' %j)
                print('Last initial image in this row is %d' %j)
                #Detect the number of remain images 
                while True:
                    os.chdir(directory_all_HS) #Move to directory of HS files
                    degree = ip.Yaw(HS_files[last_number],imu,initial_degree,initial_yaw)
                    next_degree = ip.Yaw(HS_files[last_number+1],imu,initial_degree,initial_yaw)
                    difference = abs(degree - next_degree)
                    if difference < 5:
                        print('It is fine.')
                    else:
                        print('Change point is detected')
                        break
                    last_number = last_number + 1
                a = last_number - j   
                for i in range(a):
                    os.chdir(directory_image)
                    print('Next initial image is %d' %j)
                    image = cv2.imread('%s.png' %i)
                    if i == 0:
                        all_images = np.append(initial_image,image, axis=0)
                        print(all_images.shape)
                    else:
                        all_images = np.append(all_images,image, axis=0)
                        print(all_images.shape)
                    
                    j = j + 1
                    print('j = %d' %j) 
                '''
                all_images = cv2.rotate(all_images,cv2.ROTATE_180)
                y_pixel = len(all_images)
                print(y_pixel)
                os.chdir(directory_all_HS)
                degree = ip.BigDirection(HS_files[j-a],HS_files[j],gps)
                print(degree)
                print(j-a)
                print(j)
                '''
                j_list.append(j)
                '''
                rotated_all_images = ip.big_rotation(all_images,degree,x_pixel,y_pixel_for_last)   
                    
                os.chdir(directory_image_rotated)
                cv2.imwrite('big%d.png' %k, rotated_all_images)
                '''
                del all_images    
                    
                print('Finish current row')
                break
        else:
            '''
            all_images = cv2.rotate(all_images,cv2.ROTATE_180) 
            y_pixel = len(all_images)
            print(y_pixel)
            degree = ip.BigDirection(HS_files[j-4],HS_files[j],gps)
            print(degree)
            print(j-4)
            print(j)
            '''
            j_list.append(j)
            '''
            rotated_all_images = ip.big_rotation(all_images,degree,x_pixel,y_pixel)   
                
            os.chdir(directory_image_rotated)
            s = j // number
            cv2.imwrite('big%d.png' %k, rotated_all_images)
            print('big%d.png done' %k)
            '''
            remain = flen - 1 - j
            print('remain is %d' %remain)
            j = j + 1
                  
            if remain < number:
                os.chdir(directory_image)
                initial_image = cv2.imread('%d.png' %j)
                print('Next initial image is %d' %j)
                for i in range(remain-1):
                    j = j + 1
                    print('j = %d' %j)  
                    os.chdir(directory_image)
                    image = cv2.imread('%d.png' %j)
                    if i == 0:
                        all_images = np.append(initial_image,image, axis=0)
                        print(all_images.shape)
                    else:
                        all_images = np.append(all_images,image, axis=0)
                        print(all_images.shape)
                        
                '''    
                initial_image = cv2.rotate(initial_image,cv2.ROTATE_180)   
                y_pixel = len(all_images)
                print(y_pixel)
                os.chdir(directory_all_HS)
                degree = ip.BigDirection(HS_files[flen-1-remain],HS_files[flen-1],gps)
                print(flen-1-remain)
                print(flen-1)
                '''
                j_list.append(j)
                '''
                rotated_all_images = ip.big_rotation(all_images,degree,x_pixel,y_pixel_for_last)   
                    
                os.chdir(directory_image_rotated)
                s = k + 1
                cv2.imwrite('big%d.png' %s, rotated_all_images)
                '''
                print('Finish all process')
                break
            
        continue
    break

j_list = np.array(j_list)
print(j_list)

image_len = len(j_list)
w = 1280
original_y_pixel = 1024*number
rotated_y_pixel = int(round(np.sqrt(np.power(w/2,2) + np.power(original_y_pixel/2,2)) * 2))
print(rotated_y_pixel)
with open(kml_file_name,mode='w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
    f.write('<Folder>\n')
    f.write('    <name>%s</name>\n' %kml_name) 
    f.write('    <open>1</open>\n')
    for i in range(3):
        os.chdir(directory_all_HS)
        degree = ip.BigDirection(HS_files[j_list[i]-4],HS_files[j_list[i]],gps)
        coordinate = ip.imageCoordinate_for_big(HS_files[j_list[i]],gps,offset_distance,degree,scanrate,velocity,original_y_pixel,rotated_y_pixel) ###CHANGE POINT
        imagename = 'big%d.png' %i
        f.write('    <GroundOverlay>\n')
        f.write('        <name>%d</name>\n' %i)
        f.write('        <Icon>\n')
        f.write('            <href>%s</href>\n' % imagename)
        f.write('            <viewBoundScale>1.00</viewBoundScale>\n')
        f.write('        </Icon>\n')
        f.write('        <LatLonBox>\n')
        f.write('            <north>%f</north>\n' %coordinate[0])
        f.write('            <south>%f</south>\n' %coordinate[2])
        f.write('            <east>%f</east>\n' %coordinate[3])
        f.write('            <west>%f</west>\n' %coordinate[1])
        f.write('        </LatLonBox>\n')
        f.write('    </GroundOverlay>\n')        
    f.write('</Folder>\n</kml>')
