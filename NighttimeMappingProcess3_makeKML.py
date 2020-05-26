# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:50:24 2020

@author: yacht
"""

import os
import sys
sys.path.append("D:\\Vebots\\My_master_research\\HSC\\Py_analysis_lib")
import imgprocess as ip


#Define variables
directory_all_HS = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\analysis'
kml_file_name = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\image\\New_rotated\\20200525soy_nighttime_RGB.kml'
kml_name = 'soy_nighttime_RGB'
gps = 'D:\\Vebots\\My_master_research\\HSC\\hsc20200525soy_nighttime\\raw\\gps.txt'  
offset_distance = 2
scanrate = 35
row = 2

#Make a list of all HS_files in the below directory　 
os.chdir(directory_all_HS)
HS_files = os.listdir(directory_all_HS)
ftype = type(HS_files)
flen = len(HS_files)
velocity = ip.speed(HS_files[0],HS_files[flen//row],gps)
print('velocity is %f' %velocity)
initial_degree = ip.FirstDirection(HS_files[0],gps)

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
        yaw = ip.Direction(HS_files[t-1],HS_files[t],gps)
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
