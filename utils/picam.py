'''
* Team ID : 117
* Author List : Ebey Abraham
* Filename : picam.py
* Theme : Antbot
* Functions : 
* Global Variables : NONE
'''
from imutils.video.videostream import VideoStream
import imutils
import cv2
import cv2.aruco as aruco
import numpy as np
import time

class Camera:
    def __init__(self):
        pass
    
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
        ids = []
        vs = VideoStream(usePiCamera = True).start()
        time.sleep(2)
        while len(ids) < 4:
            foundID = False #flag set when ID is detected
            ID = 0 #stores the detected ID
            #while not foundID:
            frame = vs.read()
            #frame = imutils.resize(frame, width = 400)
            aruco_list = self.detectAruco(frame)
            if len(aruco_list):
                foundID = True
                ID = list(aruco_list.keys())
                ID = ID[0]
                frame = self.markAruco(frame,aruco_list)
            if ID > 0 and ID not in ids:
                ids.append(ID)
                print("ID Detected: {}".format(ID))
        #cv2.imshow("Frame", frame)
        #key = cv2.waitKey(1) & 0xFF
        #if key == ord('q'):
        #    break
        #cv2.destroyAllWindows()
        #vs.stop()
        #return ID
    
    '''
    * Function Name : detectColor
    * Input : NONE
    * Output : returns the color of detected box
    * Logic : -
    * Example Call : detectColor()
    '''    
    def detectColor():
        vs.VideoStream().start()
        time.sleep(2)
        foundColor = False
        color = None
        while not foundColor:
            '''
            add logic here
            '''
            pass
        vs.stop()
        return color


if __name__ == "__main__":
    cam = Camera()
    cam.getArucoID()
