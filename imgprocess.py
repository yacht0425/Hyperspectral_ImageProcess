#Hyperspectral data analysis
#Format: BIL
#1024line x 151bands x 1280pixel

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import csv
import datetime
import linecache
from pyproj import Proj 
#from pyproj import Geod
import cv2
from osgeo import gdal
from osgeo import osr 


#read one hyper file
def readfile(directory,filename):
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    path = os.getcwd()
    #print("path: %s" % path)
    
    #Open image files
    file = open(filename,'rb') #Read binary data
    dbuf = np.fromfile(file,dtype=np.uint16,count=-1) #Assign the format
    file.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    
    numpy_dlc = np.array(dlc)
    
    return numpy_dlc



#read all hyper files in a directory(bands=151,350nm-1100nm)
def readallfiles(directory):
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    path = os.getcwd()
    print("path: %s" % path)
    
    #Make a list of all files in the below directory　 
    files = os.listdir(directory)
    ftype = type(files)
    flen = len(files)
    print("file type is %s" % ftype)
    print("file length = %s" % flen)
    j = len(files)

    #Open image files
    store_file = []
    global number
    number = j
    
    for i in range(number):
        fin = open(files[i],'rb') #Read binary data
        dbuf = np.fromfile(fin,dtype=np.uint16,count=-1) #Assign the format
        fin.close()
        dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
        store_file.append(dlc)

    img_list = np.array(store_file) #Convert array to np.array
    
    return number,img_list

def readallfiles_interest_lambda(directory,L):
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    path = os.getcwd()
    print("path: %s" % path)
    
    #Make a list of all files in the below directory　 
    files = os.listdir(directory)
    ftype = type(files)
    flen = len(files)
    print("file type is %s" % ftype)
    print("file length = %s" % flen)
    j = len(files)

    #Open image files
    store_file = []
    global number
    number = j
    
    for i in range(number):
        fin = open(files[i],'rb') #Read binary data
        dbuf = np.fromfile(fin,dtype=np.uint16,count=-1) #Assign the format
        fin.close()
        dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
        img_interest = dlc[:,L,:]
        store_file.append(img_interest)

    img_list = np.array(store_file) #Convert array to np.array
    
    return number,img_list

#read all hyper files in a directory(bands=121,400nm-1000nm)
def readallfilesSmall(directory):
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    path = os.getcwd()
    print("path: %s" % path)
    
    #Make a list of all files in the below directory　 
    files = os.listdir(directory)
    ftype = type(files)
    flen = len(files)
    print("file type is %s" % ftype)
    print("file length = %s" % flen)
    j = len(files)

    #Open image files
    store_file = []
    global number
    number = j
   
    for i in range(number):
        fin = open(files[i],'rb') #Read binary data
        dbuf = np.fromfile(fin,dtype=np.uint16,count=-1) #Assign the format
        fin.close()
        dlc=dbuf.reshape(1024,121,1280) #Reshape (y,L,x)
        store_file.append(dlc)

    img_list = np.array(store_file) #Convert array to np.array
    
    
    return number,img_list

def white_matrix_lambda(white_raw,lamdas,Lx,Rx,Uy,By):
    
    white_ROI = np.array(white_raw[Uy:By,lamdas,Lx:Rx])
    
    return white_ROI

#make NDVI image array from a 4-dimension list
def makeNDVIarray(number,list_d4,directory):
    #Making NDVI image   
    L1 = 86 #780nm
    L2 = 60 #650nm
    #L1 = 93 #815nm
    #L2 = 71 #705nm
    
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    directory = os.getcwd()
    print("directory: %s" % directory)
    

    for i in range(number):
        img_L1 = np.array(list_d4[i,:,L1,:], dtype=np.int16) #Convert uint16 into int16
        img_L2 = np.array(list_d4[i,:,L2,:], dtype=np.int16)
        index1 = img_L1 - img_L2 #NIR - R
        index2 = img_L1 + img_L2 #NIR + R
        img_NDVI = np.empty_like(index1) #Make an empty list
        fl_NDVI = np.array(img_NDVI,dtype=np.float32) #Convert int16 into float32
        
        for j in range(1024):
            for k in range(1280):
                if index2[j,k] > 0: #Divide index1 by index2 only in case that index2 is not 0 
                    fl_NDVI[j,k] = index1[j,k] / index2[j,k]
                else:
                    fl_NDVI[j,k] = 0

    return fl_NDVI

def makeRGBimage(filename):
    
    #Open image files
    f = open(filename,'rb') #Read binary data
    dbuf = np.fromfile(f,dtype=np.uint16,count=-1) #Assign the format
    f.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    img_list = np.array(dlc) #Convert array to np.array
    
    r = 70 #700nm
    g = 39 #545nm
    b = 26 #480nm

    img_r = img_list[:,r,:]
    img_g = img_list[:,g,:] 
    img_b = img_list[:,b,:] 

    reimg_r = img_r.transpose(1,0) #Switch x,y axis
    reimg_g = img_g.transpose(1,0) 
    reimg_b = img_b.transpose(1,0) 

    image_RGB = np.concatenate([[reimg_b],[reimg_g],[reimg_r]]) #Get together r,g,b
    reimage_RGB = image_RGB.transpose(2,1,0)  #Switch y axis for wavelength L
    rereimage_RGB = reimage_RGB * 16  #Normalization
    
    #plt.imshow(rereimage_RGB,cmap=cm.jet)
    #plt.axis('off')
    #plt.savefig(name,transparent=True,dpi=100,bbox_inches="tight",pad_inches=0.0)
    print("That's done.")

    return rereimage_RGB


def makeNDVIimage(number,list_d4,directory):
    #Making NDVI image
    L1 = 86 #780nm
    L2 = 60 #650nm
    #L1 = 93 #815nm
    #L2 = 71 #705nm
    
    #Move to target directry and Confirm current directory
    os.chdir(directory)
    directory = os.getcwd()
    print("directory: %s" % directory)
    

    for i in range(number):
        img_L1 = np.array(list_d4[i,:,L1,:], dtype=np.int16) #Convert uint16 into int16
        img_L2 = np.array(list_d4[i,:,L2,:], dtype=np.int16)

        index1 = img_L1 - img_L2 #NIR - R
        index2 = img_L1 + img_L2 #NIR + R
        img_NDVI = np.empty_like(index1) #Make an empty list
        fl_NDVI = np.array(img_NDVI,dtype=np.float32) #Convert int16 into float32

        name = "NDVI_%d" % i + ".tif"
        
       
                
        for j in range(1024):
            for k in range(1280):
                if index2[j,k] > 0: #Divide index1 by index2 only in case that index2 is not 0 
                    fl_NDVI[j,k] = index1[j,k] / index2[j,k]
                else:
                    fl_NDVI[j,k] = 0

        print(fl_NDVI)    
        plt.imshow(fl_NDVI,clim=(-1,1),cmap=cm.jet)
        plt.axis('off')
        plt.savefig(name,transparent=True,dpi=100,bbox_inches="tight",pad_inches=0.0)
        print("That's done.")
   
    return 0
 
#analize the white reference board
#the board location is (x,y) = (630,150)--(650,170)
#ls3 is [L,y,x]
def AveList_whiteSmall(ls3,luX,luY,rbX,rbY):
    
    white = []
    aveList = [] #a list of an average from 400nm to 1000nm 
    white16 = []
    for l in range(121):
        for i in range(luX,rbX):
            for j in range(luY,rbY):
                white.append(ls3[j,l,i])
        white16 = white * 16
        ave_white = np.average(white16)
        aveList.append(ave_white)
    
    return aveList

def AveList_white(ls3,luX,luY,rbX,rbY):
    
    white = []
    aveList = [] #a list of an average from 350nm to 1100nm 
    white16 = []
    for l in range(151):
        for i in range(luX,rbX):
            for j in range(luY,rbY):
                white.append(ls3[j,l,i])
        white16 = white * 16
        ave_white = np.average(white16)
        aveList.append(ave_white)
    
    return aveList

def AveList_NDVI(ls3,luX,luY,rbX,rbY):
    
    L1 = 86 #780nm
    L2 = 60 #650nm
    white_L1 = []
    white_L2 = []
    NDVI = [] #a list of an average from L1 to L2 
    white16 = []
    for i in range(luX,rbX):
        for j in range(luY,rbY):
            white_L1.append(ls3[j,L1,i])
    for i in range(luX,rbX):
        for j in range(luY,rbY):
            white_L2.append(ls3[j,L2,i])
    
    NDVI = np.array(np.stack([white_L1,white_L2]))     
    
    white16 =np.array(NDVI,dtype=np.int16)
    index1 = white16[0,:] + white16[1,:]   
    index2 = white16[0,:] - white16[1,:]
    
    NDVI = index2 / index1
    Ave_NDVI = np.average(NDVI)
    
    return Ave_NDVI

def AveList_NDVISmall(ls3,luX,luY,rbX,rbY):
    
    L1 = 76 #780nm
    L2 = 50 #650nm
    white_L1 = []
    white_L2 = []
    NDVI = [] #a list of an average from L1 to L2 
    white16 = []
    for i in range(luX,rbX):
        for j in range(luY,rbY):
            white_L1.append(ls3[j,L1,i])
    for i in range(luX,rbX):
        for j in range(luY,rbY):
            white_L2.append(ls3[j,L2,i])
    
    NDVI = np.array(np.stack([white_L1,white_L2]))     
    
    white16 =np.array(NDVI,dtype=np.int16)
    index1 = white16[0,:] + white16[1,:]   
    index2 = white16[0,:] - white16[1,:]
    
    NDVI = index2 / index1
    Ave_NDVI = np.average(NDVI)
    
    return Ave_NDVI


#make csv file for 2 dimention     
def makecsv(ls2,filename):
    fn = '%s' %filename        
    with open(fn,'w',newline='') as f:
        wt = csv.writer(f)
        wt.writerows(ls2)
        
    return 0

def makecsv_d1(ls1,filename):
    fn = '%s' %filename        
    with open(fn,'w',newline='') as f:
        wt = csv.writer(f)
        wt.writerow(ls1)
        
    return 0

def gain_RGB(directory,filename,r,g,b):
    #Open first image files to decide gain
    os.chdir(directory)
    f = open(filename,'rb') #Read binary data
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
    threshold = np.max(image_RGB)
    gain = 4000 / threshold
    print('gain = %f' %gain)
    
    return gain

def copy_RGB(directory,filename,r,g,b):
    #Open first image files to decide gain
    os.chdir(directory)
    f = open(filename,'rb') #Read binary data
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
    threshold = np.max(image_RGB)
    gain = 4000 / threshold
    image_RGB = image_RGB * gain
    
    return image_RGB

#abstract a projection at a bottom centre point in a image from a gps file
def projection(imagefile,gpsfile,OffsetDistance,OffsetAngle):
    #get the file time
    name = imagefile
    time = os.path.getmtime(name)
    
    local_time = datetime.datetime.fromtimestamp(time)
    #print('fileTime: %s' % local_time)
    s_local_time = str(local_time)
    
    gps = gpsfile
    with open(gps) as f:
        line_list = f.readlines()
    
    #Suit HS file time to GPS time. Firstly, strict constraint 22 strings match and then gradually 21, 20,... the condition is soften
    i = 22
    while True:
        need = s_local_time[:i] #Time strings of HS data for reference to the GPS time
        print('fileTimeSearch: %s' % need)       
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        print(number)
        i = i - 1
        if number > 0:
            break
     
    median = number // 2
    required_line = str(required_lines[median])
    print('gpsTime: %s' % required_line[1:24])
    N = required_line[43:56]
    E = required_line[59:72]
    fN = float(N)
    fE = float(E)
    ddddN = (fN/100 - 43) * 5 / 3 + 43
    ddddE = (fE/100 - 141) * 5 / 3 + 141
    
    #calculate offset
    dis = OffsetDistance
    ang = OffsetAngle * np.pi / 180
    if dis != 0:
        if ang != 0:
            converter = Proj(proj='utm',zone=54,ellps='GRS80')
            utm_X, utm_Y = converter(ddddE,ddddN)
            offsetX = utm_X + dis*np.sin(ang)
            offsetY = utm_Y - dis*np.cos(ang)
            ddddE,ddddN = converter(offsetX,offsetY,inverse=True)
            print('convert!')
            
    return ddddN,ddddE

def imageCoordinate(imagefile,gpsfile,offsetDistance,offsetAngle,scanrate,velo): #velo = km/h
    #get bottom coordinate
    name = imagefile
    gps = gpsfile
    dis = offsetDistance
    ang = offsetAngle * np.pi / 180
    bottom = projection(name,gps,dis,offsetAngle)
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = velo #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = 2.87 #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    #print('x_resolution = %f m' % x_resolution)
    #print('y_resolution = %f m' % y_resolution)

    #print(bottom)
    L = y_resolution * 612 * np.cos(ang) #m/pix * pix = m
    converter = Proj(proj='utm',zone=54,ellps='GRS80')
    utm_X, utm_Y = converter(bottom[1],bottom[0])
    centreX = utm_X - L * np.sin(ang)
    centreY = utm_Y + L * np.cos(ang)
    
    upperleftX = centreX - (x_resolution * 820) #transport 820pix
    upperleftY = centreY + (y_resolution * 820)
    bottomrightX = centreX + (x_resolution * 820)
    bottomrightY = centreY - (y_resolution * 820)
    #print(upperleftX,upperleftY)    
    
    upperleftE,upperleftN = converter(upperleftX,upperleftY,inverse=True)
    bottomrightE,bottomrightN = converter(bottomrightX,bottomrightY,inverse=True)
    '''
    #print('upperleftN')
    #print(upperleftN)
    #print('upperleftE')
    #print(upperleftE)
    #print('bottomrightN')
    #print(bottomrightN)
    #print('bottomrightE')
    #print(bottomrightE)
    '''
    return upperleftN,upperleftE,bottomrightN,bottomrightE

def speed(InitialImagefile,LastImagefile,gpsfile): #最初の角度yawはこれ！
    #get the file time
    initial_time = os.path.getmtime(InitialImagefile)
    last_time = os.path.getmtime(LastImagefile)
    
    #translate epoch time into local time
    initial_local_time = datetime.datetime.fromtimestamp(initial_time)
    last_local_time = datetime.datetime.fromtimestamp(last_time)
    #print('fileTime: %s' % local_time)
    s_initial_local_time = str(initial_local_time) 
    s_last_local_time = str(last_local_time) 
    #print('fileTimeSearch: %s' % need)
    
    #open a gps file
    gps = gpsfile
    with open(gps) as f:
        line_list = f.readlines()
    #print(line_list)
    #Extract lines consistent with 'need' from line_list        
    i = 22
    while True:
        need = s_initial_local_time[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    N = required_line[43:56]
    E = required_line[59:72]
    fN = float(N)
    fE = float(E)
    ddddN = (fN/100 - 43) * 5 / 3 + 43
    ddddE = (fE/100 - 141) * 5 / 3 + 141
    #print('(X1,Y1) = (%f,%f)' %(ddddN,ddddE))
    
    i = 22
    while True:
        need = s_last_local_time[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    laterN = required_line[43:56]
    laterE = required_line[59:72]
    laterfN = float(laterN)
    laterfE = float(laterE)
    laterddN = (laterfN/100 - 43) * 5 / 3 + 43
    laterddE = (laterfE/100 - 141) * 5 / 3 + 141
    
    convertor = Proj(proj='utm',zone=54,ellps='GRS80')
    utm_ddddX, utm_ddddY = convertor(ddddE,ddddN)
    utm_laterddX, utm_laterddY = convertor(laterddE,laterddN)
    #print(utm_ddddX,utm_ddddY)
    #print(utm_laterddX,utm_laterddY)
    dif_x = abs(utm_laterddX - utm_ddddX) 
    dif_y = abs(utm_laterddY - utm_ddddY) 
    distance = np.sqrt(np.power(dif_x,2) + np.power(dif_y,2))
    #print('distance: %f m' % distance)
    #print('distance between Y1 and Y2: %f m' % dif_y)
    difference_time = last_time - initial_time
    #print(difference_time)
    velocity = (distance / difference_time) *3.6 #km/h
    
    
    return velocity
    

def BigDirection(firstimagefile,lastimagefile,gpsfile): #最初の角度yawはこれ！
    #get the file time
    name_first = firstimagefile
    name_last = lastimagefile
    time_first = os.path.getmtime(name_first)
    time_last = os.path.getmtime(name_last)
    #translate epoch time into local time
    local_time_first = datetime.datetime.fromtimestamp(time_first)
    local_time_last = datetime.datetime.fromtimestamp(time_last)
    #print('fileTime: %s' % local_time)
    s_local_time_first = str(local_time_first) 
    s_local_time_last = str(local_time_last) 
    #print('fileTimeSearch: %s' % need)
    
    #open a gps file
    gps = gpsfile
    with open(gps) as f:
        line_list = f.readlines()
    #print(line_list)
    #Extract lines consistent with 'need' from line_list
    i = 22
    while True:
        need = s_local_time_first[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    N = required_line[43:56]
    E = required_line[59:72]
    fN = float(N)
    fE = float(E)
    ddddN = (fN/100 - 43) * 5 / 3 + 43
    ddddE = (fE/100 - 141) * 5 / 3 + 141
    #print('(X1,Y1) = (%f,%f)' %(ddddN,ddddE))
    
    i = 22
    while True:
        need = s_local_time_last[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    laterN = required_line[43:56]
    laterE = required_line[59:72]
    laterfN = float(laterN)
    laterfE = float(laterE)
    laterddN = (laterfN/100 - 43) * 5 / 3 + 43
    laterddE = (laterfE/100 - 141) * 5 / 3 + 141
    #print('(X2,Y2) = (%f,%f)' % (laterddN, laterddE))
    
    convertor = Proj(proj='utm',zone=54,ellps='GRS80')
    utm_ddddX, utm_ddddY = convertor(ddddE,ddddN)
    utm_laterddX, utm_laterddY = convertor(laterddE,laterddN)
    #print(utm_ddddX,utm_ddddY)
    #print(utm_laterddX,utm_laterddY)
    dif_x = utm_laterddX - utm_ddddX 
    dif_y = utm_laterddY - utm_ddddY 
    #print('distance between X1 and X2: %f m' % dif_x)
    #print('distance between Y1 and Y2: %f m' % dif_y)
    thete = np.arctan2(dif_x,dif_y)
    #print(thete)
    degree = -np.rad2deg(thete) 
    
    
    return degree

def Direction(firstimagefile,lastimagefile,gpsfile): #最初の角度yawはこれ！
    #get the file time
    name_first = firstimagefile
    name_last = lastimagefile
    time_first = os.path.getmtime(name_first)
    time_last = os.path.getmtime(name_last)
    #translate epoch time into local time
    local_time_first = datetime.datetime.fromtimestamp(time_first)
    local_time_last = datetime.datetime.fromtimestamp(time_last)
    #print('fileTime: %s' % local_time)
    s_local_time_first = str(local_time_first) 
    s_local_time_last = str(local_time_last) 
    #print('fileTimeSearch: %s' % need)
    
    #open a gps file
    gps = gpsfile
    with open(gps) as f:
        line_list = f.readlines()
    #print(line_list)
    #Extract lines consistent with 'need' from line_list
    i = 22
    while True:
        need = s_local_time_first[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    N = required_line[43:56]
    E = required_line[59:72]
    fN = float(N)
    fE = float(E)
    ddddN = (fN/100 - 43) * 5 / 3 + 43
    ddddE = (fE/100 - 141) * 5 / 3 + 141
    #print('(X1,Y1) = (%f,%f)' %(ddddN,ddddE))
    
    i = 22
    while True:
        need = s_local_time_last[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    laterN = required_line[43:56]
    laterE = required_line[59:72]
    laterfN = float(laterN)
    laterfE = float(laterE)
    laterddN = (laterfN/100 - 43) * 5 / 3 + 43
    laterddE = (laterfE/100 - 141) * 5 / 3 + 141
    #print('(X2,Y2) = (%f,%f)' % (laterddN, laterddE))
    
    convertor = Proj(proj='utm',zone=54,ellps='GRS80')
    utm_ddddX, utm_ddddY = convertor(ddddE,ddddN)
    utm_laterddX, utm_laterddY = convertor(laterddE,laterddN)
    #print(utm_ddddX,utm_ddddY)
    #print(utm_laterddX,utm_laterddY)
    dif_x = utm_laterddX - utm_ddddX 
    dif_y = utm_laterddY - utm_ddddY 
    #print('distance between X1 and X2: %f m' % dif_x)
    #print('distance between Y1 and Y2: %f m' % dif_y)
    thete = np.arctan2(dif_x,dif_y)
    #print(thete)
    degree = -np.rad2deg(thete) 
    
    
    return degree

#Extract direction in the first image from a gps file
def FirstDirection(firstimagefile,gpsfile): #最初の角度yawはこれ！
    #get the file time
    name = firstimagefile
    time = os.path.getmtime(name)
    
    #translate epoch time into local time
    local_time = datetime.datetime.fromtimestamp(time)
    #print('fileTime: %s' % local_time)
    s_local_time = str(local_time) 
    #print('fileTimeSearch: %s' % need)
    
    #open a gps file
    gps = gpsfile
    with open(gps) as f:
        line_list = f.readlines()
    #print(line_list)
    #Extract lines consistent with 'need' from line_list        
    i = 22
    while True:
        need = s_local_time[:i] #until 21 is the required time strings
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
        
    median = number // 2
    required_line = str(required_lines[median])
    #print('gpsTime: %s' % required_line[1:24])
    N = required_line[43:56]
    E = required_line[59:72]
    fN = float(N)
    fE = float(E)
    ddddN = (fN/100 - 43) * 5 / 3 + 43
    ddddE = (fE/100 - 141) * 5 / 3 + 141
    #print('(X1,Y1) = (%f,%f)' %(ddddN,ddddE))
    
    #read a line which is 1000 seconds later 
    required_line_low_list = [i for i, line in enumerate(line_list) if required_line in line]
    required_line_low = required_line_low_list[0]
    #print('low number: %s' % required_line_low)
    needed_line_low = required_line_low + 10000 #take a GPS point around the end
    needed_line = linecache.getline(gps, needed_line_low)
    laterN = needed_line[43:56]
    laterE = needed_line[59:72]
    laterfN = float(laterN)
    laterfE = float(laterE)
    laterddN = (laterfN/100 - 43) * 5 / 3 + 43
    laterddE = (laterfE/100 - 141) * 5 / 3 + 141
    #print('(X2,Y2) = (%f,%f)' % (laterddN, laterddE))
    
    convertor = Proj(proj='utm',zone=54,ellps='GRS80')
    utm_ddddX, utm_ddddY = convertor(ddddE,ddddN)
    utm_laterddX, utm_laterddY = convertor(laterddE,laterddN)
    #print(utm_ddddX,utm_ddddY)
    #print(utm_laterddX,utm_laterddY)
    dif_x = utm_laterddX - utm_ddddX 
    dif_y = utm_laterddY - utm_ddddY 
    #print('distance between X1 and X2: %f m' % dif_x)
    #print('distance between Y1 and Y2: %f m' % dif_y)
    thete = np.arctan2(dif_x,dif_y)
    #print(thete)
    degree = -np.rad2deg(thete) 
    
    
    return degree

#abstract direction in a image from a gps file
def firstYaw(firstimagefile,imufile): #Yaw関数のために使う
    #get the file time
    name = firstimagefile
    time = os.path.getmtime(name)
    
    #translate epoch time into local time
    local_time = datetime.datetime.fromtimestamp(time)
    #print('fileTime: %s' % local_time)
    s_local_time = str(local_time)
    #print('fileTimeSearch: %s' % need)
    
    #open a imu file
    imu = imufile
    with open(imu) as f:
        line_list = f.readlines()
    
    #abstract lines consistent with 'need' from line_list        
    i = 22
    while True:
        need = s_local_time[:i] #until 21 is the required time strings 
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('imuTime: %s' % required_line[1:24])
    yaw = required_line[34:41]
    initialyaw = float(yaw)
    #print(initialyaw)
    
    return initialyaw

def Yaw(imagefile,imufile,initialDirection,initialYaw):
    #get the file time
    name = imagefile
    time = os.path.getmtime(name)
    
    #translate epoch time into local time
    local_time = datetime.datetime.fromtimestamp(time)
    #print('fileTime: %s' % local_time)
    s_local_time = str(local_time)
    #print('fileTimeSearch: %s' % need)
    
    #open a imu file
    imu = imufile
    with open(imu) as f:
        line_list = f.readlines()
    
    #abstract lines consistent with 'need' from line_list        
    i = 22
    while True:
        need = s_local_time[:i] #until 21 is the required time strings 
        required_lines = [line.strip() for line in line_list if need in line]
        number = len(required_lines)
        i = i - 1
        if number != 0:
            break
    median = number // 2
    required_line = str(required_lines[median])
    #print('imuTime: %s' % required_line[1:24])
    yaw = required_line[34:41]
    fyaw = float(yaw)
    
    current_direction = initialDirection + (fyaw - initialYaw)
    
    return current_direction

def rotation(img,degree,scanrate,velo,width):    
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = velo #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = width #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    #print('x_resolution = %f m' % x_resolution)
    #print('y_resolution = %f m' % y_resolution)
    
    ratio = y_resolution / x_resolution
    #print('ratio = %f' %ratio)
    if(0.9 < ratio < 1.1):
        w = 1280
        print('Not modify.')
    else:
        img = cv2.resize(img,(int(x_pixel//ratio),int(y_pixel)))
        print('Modify!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        w = int(x_pixel//ratio)
        print('x_pixel is %d' %w)
    
    #assign w and h pixels
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,degree,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    img_affine = cv2.warpAffine(img,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    r_channel = img_affine[:,:,0]
    g_channel = img_affine[:,:,1]
    b_channel = img_affine[:,:,2]
    
    #make alpha channel
    alpha = np.ones(b_channel.shape[:2], np.uint8) * 255
    for i in range(w_after):
        for j in range(w_after):    
            if r_channel[i][j] == 0:
                if g_channel[i][j] == 0:
                    if b_channel[i][j] == 0:
                        alpha[i][j] = 0
    
    #concatenate r, g, b and alpha channel
    new = cv2.merge((r_channel,g_channel,b_channel,alpha))
    
    return new

def big_rotation(img,degree,x_pixel,y_pixel):    
    
    #assign w and h pixels
    w = x_pixel
    h = y_pixel
    h_after = int(round(np.sqrt(np.power(w/2,2) + np.power(h/2,2)) * 2))
    w_after = int(round(np.sqrt(np.power(w/2,2) + np.power(h/2,2)) * 2))
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,degree,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    img_affine = cv2.warpAffine(img,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    r_channel = img_affine[:,:,0]
    g_channel = img_affine[:,:,1]
    b_channel = img_affine[:,:,2]
    
    #make alpha channel
    alpha = np.ones(b_channel.shape[:2], np.uint8) * 255
    for i in range(w_after):
        for j in range(w_after):    
            if r_channel[i][j] == 0:
                if g_channel[i][j] == 0:
                    if b_channel[i][j] == 0:
                        alpha[i][j] = 0
    
    #concatenate r, g, b and alpha channel
    new = cv2.merge((r_channel,g_channel,b_channel,alpha))
    
    return new


def makeRGBA(filename,degree,imagename,brightness):    
    #read a file
    name = filename
    img = makeRGBimage(name)
    ls = np.array(img*brightness) #3 times brighter than original one
    
    #give a rotation angle
    angle = degree
    
    #angle_rad = angle/180.0 * np.pi
    #w_after = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
    #h_after = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
    
    #assign w and h pixels
    w = 1280
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    img_affine = cv2.warpAffine(ls,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    r_channel = img_affine[:,:,0]
    g_channel = img_affine[:,:,1]
    b_channel = img_affine[:,:,2]
    
    #make alpha channel
    alpha = np.ones(b_channel.shape[:2], np.uint16) * 65535
    for i in range(w_after):
        for j in range(w_after):    
            if b_channel[i][j] == 0:
                alpha[i][j] = 0
    
    #concatenate r, g, b and alpha channel
    new = cv2.merge((r_channel,g_channel,b_channel,alpha))
    
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',new)
    #cv2.waitKey(0)
    cv2.imwrite('%s' %imagename,new)
    #cv2.destroyAllWindows()
    
    return 0 

def makeRGBA_ForNight(filename,degree,imagename,brightness,scanrate,velo):    
    #read a file
    name = filename
    img = makeRGBimage(name)
    ls = np.array(img*brightness) #3 times brighter than original one
    print(ls.shape)
    #give a rotation angle
    angle = degree
    
    #cut from 0 to 350 and from 900 to 1280
    for i in range(0,350):
        ls[:,i,:] = 0
    for j in range(900,1280):
        ls[:,j,:] = 0
                    
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = velo #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = 2.87 #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    print('x_resolution = %f m' % x_resolution)
    print('y_resolution = %f m' % y_resolution)
    
    ratio = y_resolution / x_resolution
    print('ratio = %f' %ratio)
    if(0.9 < ratio < 1.1):
        w = 1280
        print('Not modify.')
    else:
        ls = cv2.resize(ls,(int(x_pixel//ratio),int(y_pixel)))
        print('Modify!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        w = int(x_pixel//ratio)
        
        
    #assign w and h pixels
    
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    img_affine = cv2.warpAffine(ls,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    r_channel = img_affine[:,:,0]
    g_channel = img_affine[:,:,1]
    b_channel = img_affine[:,:,2]
    
    #make alpha channel
    alpha = np.ones(b_channel.shape[:2], np.uint16) * 65535
    for i in range(w_after):
        for j in range(h_after):    
            if g_channel[i][j] < 7000:
                if r_channel[i][j] < 7000:
                    alpha[i][j] = 0
    
    #concatenate r, g, b and alpha channel
    new = cv2.merge((r_channel,g_channel,b_channel,alpha))
    
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',new)
    #cv2.waitKey(0)
    cv2.imwrite('%s' %imagename,new)
    #cv2.destroyAllWindows()
    
    return 0 

def makeBMP_ForNight(filename,degree,imagename,brightness,scanrate,velo,WL):    
    #read a file
    name = filename
    #Open image files
    f = open(name,'rb') #Read binary data
    dbuf = np.fromfile(f,dtype=np.uint16,count=-1) #Assign the format
    f.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    img_list = np.array(dlc) #Convert array to np.array
    L = int((WL - 350) / 5)
    img = img_list[:,L,:]
    
    ls = np.array(img*brightness, dtype=np.uint16) #3 times brighter than original one
    gray = []
    for i in range(3):
        gray.append
    
    x = cv2.imread(ls)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img',x)
    cv2.waitKey(0)
    cv2.imwrite('D:\\Vebots\\My_master_research\\HSC\\hsc20200109kitchenpaper\\image\\NonCalibration.png',b)
    cv2.destroyAllWindows()
    print("That's done.")
    '''
    fig, ax = plt.subplots()
    ax.imshow(ls, cmap='gray')
    plt.show()
    '''
    '''
    #give a rotation angle
    angle = degree
    #cut from 0 to 350 and from 900 to 1280
    for i in range(0,350):
        ls[:,i] = 0
    for j in range(900,1280):
        ls[:,j] = 0
                    
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = velo #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = 2.87 #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    print('x_resolution = %f m' % x_resolution)
    print('y_resolution = %f m' % y_resolution)
    
    ratio = y_resolution / x_resolution
    print('ratio = %f' %ratio)
    if(0.9 < ratio < 1.1):
        w = 1280
        print('Not modify.')
    else:
        ls = cv2.resize(ls,(int(x_pixel//ratio),int(y_pixel)))
        print('Modify!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        w = int(x_pixel//ratio)
        
        
    #assign w and h pixels
    
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    img_affine = cv2.warpAffine(ls,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    r_channel = img_affine[:,:,0]
    g_channel = img_affine[:,:,1]
    b_channel = img_affine[:,:,2]
    
    #make alpha channel
    alpha = np.ones(b_channel.shape[:2], np.uint16) * 65535
    for i in range(w_after):
        for j in range(h_after):    
            if g_channel[i][j] < 7000:
                if r_channel[i][j] < 7000:
                    alpha[i][j] = 0
    
    #concatenate r, g, b and alpha channel
    new = cv2.merge((r_channel,g_channel,b_channel,alpha))
    
    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow('img',new)
    #cv2.waitKey(0)
    cv2.imwrite('%s' %imagename,new)
    #cv2.destroyAllWindows()
    '''
    return 0 

def imageCoordinate_for_modify(imagefile,gpsfile,offsetDistance,offsetAngle,scanrate,velo): #velo = km/h
    #get bottom coordinate
    name = imagefile
    gps = gpsfile
    dis = offsetDistance
    ang = offsetAngle * np.pi / 180
    top = projection(name,gps,dis,offsetAngle)
    
    #Calculate resolution
    y_pixel = 1024
    ms_speed = velo / 3.6 #m/s
    y_width = y_pixel / scanrate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    y_resolution = y_width / y_pixel #(m/pix)
    x_resolution = y_resolution 
    #print('x_resolution = %f m' % x_resolution)
    #print('y_resolution = %f m' % y_resolution)

    #print(bottom)
    L = y_resolution * 512  #m/pix * pix = m 最初の2項は新たな画像におけるresolution
    converter = Proj(proj='utm',zone=54,ellps='GRS80')
    top_X, top_Y = converter(top[1],top[0])
    centreX = top_X + L * np.sin(ang)
    centreY = top_Y - L * np.cos(ang)
    
    upperleftX = centreX - (x_resolution * 820) #transport 820pix
    upperleftY = centreY + (y_resolution * 820)
    bottomrightX = centreX + (x_resolution * 820)
    bottomrightY = centreY - (y_resolution * 820)
    #print(upperleftX,upperleftY)    
    
    upperleftE,upperleftN = converter(upperleftX,upperleftY,inverse=True)
    bottomrightE,bottomrightN = converter(bottomrightX,bottomrightY,inverse=True)
    '''
    print('upperleftN')
    print(upperleftN)
    print('upperleftE')
    print(upperleftE)
    print('bottomrightN')
    print(bottomrightN)
    print('bottomrightE')
    print(bottomrightE)
    '''
    return upperleftN,upperleftE,bottomrightN,bottomrightE

def imageCoordinate_for_big(imagefile,gpsfile,offsetDistance,offsetAngle,scanrate,velo,original_y_pixel,rotated_y_pixel): #velo = km/h
    #get bottom coordinate
    name = imagefile
    gps = gpsfile
    dis = offsetDistance
    ang = np.rad2deg(offsetAngle)
    top = projection(name,gps,dis,offsetAngle)
    converter = Proj(proj='utm',zone=54,ellps='GRS80')
    top_X, top_Y = converter(top[1],top[0])
    
    #Calculate resolution
    ms_speed = velo / 3.6 #m/s
    y_width = original_y_pixel / scanrate * ms_speed #m
    y_resolution = y_width / original_y_pixel #(m/pix)
    x_resolution = y_resolution 
    h = original_y_pixel
    
    #print(top)
    L = y_resolution * (h / 2)  #m/pix * pix = m 最初の2項は新たな画像におけるresolution
    centre_X = top_X + L * np.sin(ang)
    centre_Y = top_Y - L * np.cos(ang)
    
    topleftX = centre_X - (x_resolution * rotated_y_pixel // 2)
    topleftY = centre_Y + (y_resolution * rotated_y_pixel // 2)
    bottomrightX = centre_X + (x_resolution * rotated_y_pixel // 2)
    bottomrightY = centre_Y - (y_resolution * rotated_y_pixel // 2)
    #print(topleftX,topleftY)    
    
    topleftE,topleftN = converter(topleftX,topleftY,inverse=True)
    bottomrightE,bottomrightN = converter(bottomrightX,bottomrightY,inverse=True)
    
    print('topleftN')
    print(topleftN)
    print('topleftE')
    print(topleftE)
    print('bottomrightN')
    print(bottomrightN)
    print('bottomrightE')
    print(bottomrightE)
    
    return topleftN,topleftE,bottomrightN,bottomrightE

def MakeRasterRGBA(filename,scanrate,speed,Lat,Lon,yaw,tiffname):
    
    #read a file
    name = filename
    #Open image files
    f = open(name,'rb') #Read binary data
    dbuf = np.fromfile(f,dtype=np.uint16,count=-1) #Assign the format
    f.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    img = np.array(dlc)
    
    WL1 = 700
    WL2 = 545
    WL3 = 435
    L1 = int((WL1 - 350) / 5)
    L2 = int((WL2 - 350) / 5)
    L3 = int((WL3 - 350) / 5)
    
    b1 = img[:,L1,:] // 16
    b2 = img[:,L2,:] // 16
    b3 = img[:,L3,:] // 16
    
    #cut from 0 to 350 and from 900 to 1280
    for i in range(0,350):
        b1[:,i] = 0
        b2[:,i] = 0
        b3[:,i] = 0
    for j in range(900,1280):
        b1[:,j] = 0
        b2[:,j] = 0
        b3[:,j] = 0
        
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = speed #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = 2.87 #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    #print('x_resolution = %f m' % x_resolution)
    #print('y_resolution = %f m' % y_resolution)
    
    
    #projection
    converter = Proj(proj='utm',zone=54,ellps='WGS84')
    utm_x,utm_y = converter(Lon,Lat)
    
    
    #assign w and h pixels
    w = 1280
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    angle = yaw
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    b1_affine = cv2.warpAffine(b1,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    b2_affine = cv2.warpAffine(b2,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    b3_affine = cv2.warpAffine(b3,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    #make alpha channel 
    alpha = np.ones(b1_affine.shape, np.uint16) * 255
    for i in range(w_after):
        for j in range(h_after):    
            if b1_affine[i][j] < 10: #less than 10 are 0
                if b2_affine[i][j] < 10:
                    alpha[i][j] = 0
    
    
    imagename = tiffname
    columns = w_after
    rows = h_after
    driver = gdal.GetDriverByName('Gtiff')
    outRaster = driver.Create(imagename,columns, rows, 4, gdal.GDT_Byte)
    outRaster.SetGeoTransform((utm_x,x_resolution,0,utm_y,0,-y_resolution))
    outRaster.GetRasterBand(1).WriteArray(b1_affine)
    outRaster.GetRasterBand(2).WriteArray(b2_affine)
    outRaster.GetRasterBand(3).WriteArray(b3_affine)
    outRaster.GetRasterBand(4).WriteArray(alpha)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(6691) #UTM zone
    outRaster.FlushCache()
    outRaster = None
    print('finish')
    
    return 0

def MakeRasterIndex(filename,scanrate,speed,Lat,Lon,yaw,tiffname,L1,L2):
    
    #read a file
    name = filename
    #Open image files
    f = open(name,'rb') #Read binary data
    dbuf = np.fromfile(f,dtype=np.uint16,count=-1) #Assign the format
    f.close()
    dlc=dbuf.reshape(1024,151,1280) #Reshape (y,L,x)
    img = np.array(dlc)
    
    WL1 = L1
    WL2 = L2
    #WL3 = 435
    L1 = int((WL1 - 350) / 5)
    L2 = int((WL2 - 350) / 5)
    #L3 = int((WL3 - 350) / 5)
    
    b1 = img[:,L1,:] // 16
    b2 = img[:,L2,:] // 16
    #b3 = img[:,L3,:] // 16
    
    #cut from 0 to 350 and from 900 to 1280
    for i in range(0,350):
        b1[:,i] = 0
        b2[:,i] = 0
        #b3[:,i] = 0
    for j in range(900,1280):
        b1[:,j] = 0
        b2[:,j] = 0
        #b3[:,j] = 0
        
    
    #Calculate resolution
    x_pixel = 1280 #(pixel)
    scan_rate = scanrate #(line/sec)
    y_pixel = 1024
    velocity = speed #km/h
    ms_speed = velocity / 3.6 #m/s
    x_width = 2.87 #(m) on the ground 実測値！
    y_width = y_pixel / scan_rate * ms_speed #m
    #print('x_width = %f m' % x_width)
    #print('y_width = %f m' % y_width)
    x_resolution = x_width / x_pixel #(m/pix)
    y_resolution = y_width / y_pixel 
    #print('x_resolution = %f m' % x_resolution)
    #print('y_resolution = %f m' % y_resolution)
    
    
    #projection
    converter = Proj(proj='utm',zone=54,ellps='WGS84')
    utm_x,utm_y = converter(Lon,Lat)
    
    
    #assign w and h pixels
    w = 1280
    h = 1024
    w_after = 1640
    h_after = 1640
    size_after = (w_after,h_after)
    
    #assign rotation center to image center 
    center = (w/2,h/2)
    angle = yaw
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center,angle,scale)
    
    #transportation matrix
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] - w/2 + w_after/2
    affine_matrix[1][2] = affine_matrix[1][2] - h/2 + h_after/2
    
    b1_affine = cv2.warpAffine(b1,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    b2_affine = cv2.warpAffine(b2,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    #b3_affine = cv2.warpAffine(b3,affine_matrix, size_after,flags=cv2.INTER_CUBIC)
    
    #make alpha channel 
    alpha = np.ones(b1_affine.shape, np.uint16) * 255
    for i in range(w_after):
        for j in range(h_after):    
            if b1_affine[i][j] < 10: #less than 10 are 0
                if b2_affine[i][j] < 10:
                    alpha[i][j] = 0
    
    
    imagename = tiffname
    columns = w_after
    rows = h_after
    driver = gdal.GetDriverByName('Gtiff')
    outRaster = driver.Create(imagename,columns, rows, 4, gdal.GDT_Byte)
    outRaster.SetGeoTransform((utm_x,x_resolution,0,utm_y,0,-y_resolution))
    outRaster.GetRasterBand(1).WriteArray(b1_affine)
    outRaster.GetRasterBand(2).WriteArray(b2_affine)
    #outRaster.GetRasterBand(3).WriteArray(b3_affine)
    outRaster.GetRasterBand(4).WriteArray(alpha)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(6691) #UTM zone
    outRaster.FlushCache()
    outRaster = None
    print('finish')
    
    return 0
