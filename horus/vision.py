#!/usr/bin/python

import cv2
import numpy as np

class ColorMaskBuilder(object):

    def __init__(self,color,options):
        self.__color = color
        self.__options = options

    def update_parameters(self,color,options):
        self.__options = options
        self.__color = color

    def generate_mask(self,image):
        l_h = self.__color[0] - self.__options["hue-tolerance"]
        l_h = l_h if l_h >= 0 else 0
        l_s = self.__color[1] - self.__options["saturation-tolerance"]
        l_s = l_s if l_s >= 0 else 0
        l_v = self.__color[2] - self.__options["value-tolerance"]
        l_v = l_v if l_v >= 0 else 0

        u_h = self.__color[0] + self.__options["hue-tolerance"]
        u_h = u_h if u_h <= 255 else 255
        u_s = self.__color[1] + self.__options["saturation-tolerance"]
        u_s = u_s if u_s <= 255 else 255
        u_v = self.__color[2] + self.__options["value-tolerance"]
        u_v = u_v if u_v <= 255 else 255


        lower = np.array([l_h,l_s,l_v],dtype="uint8")
        upper = np.array([u_h,u_s,u_v],dtype="uint8")

        mask = cv2.inRange(image,lower,upper)

        kn = np.ones((3,3),np.uint8)
        mask = cv2.erode(mask,kn)

        contour_map = np.ones((800,600),np.uint8)
        contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        x = None
        y = None

        for contour in contours:
            area = cv2.contourArea(contour)
            approx = cv2.approxPolyDP(contour,0.02*cv2.arcLength(contour,True),True)

            #TODO Add param to control
            if area > 25 and len(approx)==4:
                cv2.drawContours(contour_map,[approx],0,(255,0,0),3)
                moments = cv2.moments(approx)
                x = int(moments["m10"]/moments["m00"])
                y = int(moments["m01"]/moments["m00"])


        return mask,contour_map,(x,y)
