#!/usr/bin/python
#coding: utf-8

import cv2
import numpy as np
import os

class InputManager(object):

    def __init__(self,id):
        self.__cam = cv2.VideoCapture(id)
        if not self.__cam.isOpened():
            raise IOError("La Webcam ne peut être ouverte")

    def propagate(self):
        success,frame = self.__cam.read()
        if success:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            return frame
        else:
            raise IOException("Impossible de lire la Webcam")

    def close(self):
        self.__cam.release()


class OutputManager(object):

    def __init__(self,path):
        self.__path = path
        if os.path.exists(path):
            os.remove(path)
        descriptor = os.mkfifo(path)

    def close(self):
        os.remove(self.__path)

    def propagate(self,position,rotation):
        if len(position)>=3 and len(rotation)>=3:
            session = open(self.__path,'w')
            session.write('%f %f %f %f %f %f' % (position[0],position[1],position[2],rotation[0],rotation[1],rotation[2]))
            session.close()
        else:
            raise Exception("Le format des sorties est incorrect")
