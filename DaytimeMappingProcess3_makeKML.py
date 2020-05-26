# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:51:16 2020

@author: yacht
"""

import os
import sys
sys.path.append("D:\\Vebots\\My_master_research\\HSC\\Py_analysis_lib")
import imgprocess as ip


#Define variables
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\analysis'
kml_file_name = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\image\\rotated_RGB\\20200521_wheat_daytime_RGB.kml'
kml_name = 'wheat_daytime_RGB'
imu = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\imu.txt' 
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200521wheat_daytime\\raw\\gps.txt'  
offset_distance = 2
scanrate = 110
velocity = 0.36 #0.3でやったらなぜかアナがたくさんあいた．実際のスピードが違ったのか．．．．？


#Make a list of all HS_files in the below directory　 
os.chdir(directory_all_HS)
HS_files = os.listdir(directory_all_HS)
ftype = type(HS_files)
flen = len(HS_files)

initial_degree = ip.FirstDirection(HS_files[0],gps)
initial_yaw = ip.firstYaw(HS_files[0],imu)

with open(kml_file_name,mode='w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
    f.write('<Folder>\n')
    f.write('    <name>%s</name>\n' %kml_name) 
    f.write('    <open>1</open>\n')
    os.chdir(directory_all_HS)
    velocity = ip.speed(HS_files[0],HS_files[1],gps)
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
        os.chdir(directory_all_HS)
        velocity = ip.speed(HS_files[i],HS_files[i+1],gps)
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
