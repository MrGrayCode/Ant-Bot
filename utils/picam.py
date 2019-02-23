'''
* Team ID : 117
* Author List : Ebey Abraham, Akshatha Nayak, Anandhu Udayakumar
* Filename : picam.py
* Theme : Antbot
* Functions : detectAruco(img), markAruco(img,aruco_list), getArucoID(), getArucoBits()
* Global Variables : NONE
'''
from imutils.video.videostream import VideoStream
import imutils
import cv2
import cv2.aruco as aruco
import numpy as np
import time
import csv
import pandas as pd
import numpy as np

class Camera:
    def __init__(self):
        self.IDs = []
        #range for red color
        self.lower_red = np.array([160,100,0])
        self.upper_red = np.array([180,255,255])
        #range for blue color
        self.lower_blue = np.array([100,100,0])
        self.upper_blue = np.array([140,255,255])
        #range for green color
        self.lower_green = np.array([40,100,0])
        self.upper_green = np.array([80,255,255])
        #range for yellow color
        self.lower_yellow = np.array([10,100,100])
        self.upper_yellow = np.array([30,255,255])
        
        

    '''
    * Function Name : detectAruco
    * Input : img-> image to detect aruco marker from
    * Output : returns the detected aruco id and its corner as a dictionary
    * Logic : check that the image frame has only one aruco marker and return the id and corner list as a key value pair
    * Example Call : detectAruco(img)
    '''
    def detectAruco(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #create aruco dictionary of 7x7 bits and 1000 combinations
        aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_1000)
        parameters = aruco.DetectorParameters_create()
        #list of corners and ids
        corners, ids, _ = aruco.detectMarkers(gray,aruco_dict,parameters = parameters)
        aruco_list = {} #stores pairs of aruco id and corresponding corners
        #check that only one aruco marker is there and return the aruco id
        if len(corners) == 1:
            aruco_list[ids[0][0]] = corners[0][0]
        return aruco_list

    '''
    * Function Name : markAruco
    * Input : img-> image to detect aruco marker from
              aruco_list -> dictionary of aruco corners indexed by the aruco ID
    * Output : returns the image with the marked corners
    * Logic : find the center of the aruco marker by finding the mean and mark the center and the corners
    * Example Call : markAruco(img,aruco_list)
    '''
    def markAruco(self,img,aruco_list):
        ids = aruco_list.keys()
        font = cv2.FONT_HERSHEY_SIMPLEX
        for id in ids:
            corners = aruco_list[id]
            center = corners[0] + corners[1] + corners[2] + corners[3]
            center[:] = [int(x/4) for x in center]
            center = tuple(center)
            #marking the points
            cv2.circle(img,center,1,(0,0,255),8)
            cv2.circle(img,tuple(corners[0]),1,(0,0,255),8)
            cv2.circle(img,tuple(corners[1]),1,(0,255,0),8)
            cv2.circle(img,tuple(corners[2]),1,(255,0,0),8)
        return img

    '''
    * Function Name : getArucoID
    * Input : NONE
    * Output : returns the detected aruco ID
    * Logic : loop the camera feed till a aruco marker id detected by detectAruco
    * Example Call : getArucoID()
    '''
    def getArucoID(self):
        vs = VideoStream(usePiCamera = True).start()
        time.sleep(0.5)
        ids = []
        while len(ids) < 4:
            ID = 0 #stores the detected ID
            frame = vs.read()
            aruco_list = self.detectAruco(frame)
            if len(aruco_list):
                foundID = True
                ID = list(aruco_list.keys())
                ID = ID[0]
            #check that the detected ID is not repeated and add to the list of ids
            if ID > 0 and ID not in ids:
                ids.append(ID)
                #self.IDs.append(bin(ID)[2:]) #store ID in binary format
                print("ID Detected: {}".format(ID))
        vs.stop()
        
    def getColor(self):
        vs = VideoStream(usePiCamera = True).start()
        time.sleep(0.5)
        count = 3
        colors = {'r':0,'b':0,'g':0,'y':0}
        while count:
            count -= 1
            frame = vs.read()
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask_red = cv2.inRange(hsv,self.lower_red,self.upper_red)
            mask_blue = cv2.inRange(hsv,self.lower_blue,self.upper_blue)
            mask_green = cv2.inRange(hsv,self.lower_green,self.upper_green)
            mask_yellow = cv2.inRange(hsv,self.lower_yellow,self.upper_yellow)
            
            colors['r'] = cv2.countNonZero(mask_red)
            colors['b'] = cv2.countNonZero(mask_blue)
            colors['g'] = cv2.countNonZero(mask_green)
            colors['y'] = cv2.countNonZero(mask_yellow)
            
            #res = cv2.bitwise_and(frame,frame,mask = mask_yellow)
            #cv2.imshow("Res",res)
            #cv2.waitKey(10)
        vs.stop()
        print(colors)
        for color in colors:
            if colors[color] > 5000:
                return color
        return 'x'
            
		
if __name__ == "__main__":
    cam = Camera()
    res = cam.getColor()
    print(res)
