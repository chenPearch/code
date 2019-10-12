# coding=utf-8
# version 2.0
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import os
from helperFile import helperClass
import math
from networktables import NetworkTables
import time

print("current version  - 5")

#fov = 39.63915899594
FOV = 27.7665349671
tan_frame = math.tan(math.radians(FOV))
CAM_PATH = 'http://root:root@10.45.86.12/mjpg/video.mjpg'
DEBUG = False   #<------------------------------
ISPI = True

#creates a list of the img names from
#the #"v" folder
def getCam(Path):
    flag = False
    while(not flag):
        print("connecting to camera")
        cap = cv2.VideoCapture(Path) #<
        # cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture('http://root:root@192.168.1.21/mjpg/video.mjpg')
        if(cap.isOpened()):
            flag = True
    return cap


def getStartingPointBySlope(cnts):
        i = 0
        #gets the delta X and Y and finds the slope
        dx, dy = cv2.fitLine(cnts[i],cv2.DIST_L2 , 0, 0.01, 0.01)[:2]
        m = dy / dx
        #the y axis is inverted so the slope is also inverted
        if m < 0:
            i =1
        return i
#creates the class obj


if(not DEBUG):
    ISPI = True

if(ISPI):
    jSON_PATH = "/home/pi/frcvision/HSVdata.json"
else:
    jSON_PATH = "HSVdata.json"           

t = helperClass("slidersWin",ISPI,jSON_PATH)



cap = getCam(CAM_PATH)



if DEBUG:
    #creates the sliders
    sliders = t.createTrackBars()



NetworkTables.initialize(server = "10.45.86.2")
#NetworkTables.setClientMode()
table = NetworkTables.getTable('imgProc')
table.putValue("angle", 0)
table.putValue("distance",0)


difCounter = 0
imgC = 0

while(True):
    # try:
        smallestDistance = 10000
        start_time = time.time()
        try:
            _,frame = cap.read()
        except:
            print("couldnt read frame")
            cap = getCam(CAM_PATH)
            continue

        # frame = cv2.imread(mypath+images[imgC]) #<
        # frame = cv2.GaussianBlur(frame,(5,5),0)
        f_height , f_width = frame.shape[:2]
        if DEBUG:
            t.writeHSVvals()
        upper,lower = t.getHSV()
        midFrame = f_width/2 - 15 #koksinel     #<-------------------------------------------------------------------
        bitImg,mask,_ = t.createMask(frame,lower,upper)
        contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        filterCnts = []
        #filter the contuores
        for cnt in contours:
            S = cv2.contourArea(cnt)
            if S > 70:
                filterCnts.append(cnt)
                
        #if the number of filter contours makes sense
        if len(filterCnts) > 1 and len(filterCnts) < 25:
            #filter the contours from right to left
            filterCnts = t.sort_contours(filterCnts)
            #get the while loop's starting point based on the
            #first contoure oriantion
            startIndex = getStartingPointBySlope(filterCnts)
            #a list of all the mid x values from the pic
            midx = []
            dis = []
            #finds the mid points. and add them to a list
            while startIndex < len(filterCnts)-1:
                x1,y1 = cv2.boundingRect(filterCnts[startIndex])[:2]
                x,y2,w = cv2.boundingRect(filterCnts[startIndex+1])[:3]
                x2 = x+w
                #finds the sdif and appends by that
                dis.append(t.distance(x1,y1,x2,y2))
                midx.append((x1+x2)/2)                
                #if counter is bigger then 5 the restart it
                if DEBUG:
                    cv2.line(bitImg,(int((x1+x2)/2),0),(int((x1+x2)/2),1000),(0,0,255),2)
                    cv2.line(bitImg,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2)
                #end of loop
                #skips 1 cnt 
                startIndex += 2
            #finds the mid x with the clousest  
            if(len(dis)>0):
                for i in range(len(dis)):
                    tan_alfa = (midx[i] - midFrame)*tan_frame/midFrame
                    Fdis = dis[i]
                    #print Fdis
                    d1 = (20.32*midFrame)/(Fdis*tan_frame)
                    d2 = d1/math.cos(tan_alfa)
                    #print "first",d2
                    if(2 < smallestDistance):
                        smallestDistance = d2
                        alfa = math.degrees(math.atan(tan_alfa))
                    else:
                        difCounter += 1
                        
                table.putValue('angle', alfa)
                print(alfa)
                # print "second", distance1
                #print(alfa)
                # print "running"
                # table.putValue('distance', d2)
            else:
                table.putValue('angle', -999)
        if(not cap.isOpened()):
            continue


        end_time = time.time()
        k = cv2.waitKey(1)
        if DEBUG:
            cv2.line(bitImg,(int(midFrame),0),(int(midFrame),1000),(255,0,0)) #<---
            cv2.imshow("bitImg",bitImg)        #<-----
            cv2.imshow("mask",mask)        #<-----
            if k == 27:
                break
    # except:
    #     table.putValue('angle', -999)
    #     print("------excepted.------")
    #     # cap = getCam(CAM_PATH)
cv2.destroyAllWindows()
os._exit(0)