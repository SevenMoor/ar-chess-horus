#!/usr/bin/python
#coding: utf-8

import cv2
import numpy as np
import os
import time

class InputManager(object):

    def __init__(self,id):
        self.__cam = cv2.VideoCapture(id)
        cv2.VideoWriter_fourcc(*'XVID')
        self.__cam.set(cv2.CAP_PROP_FPS, 20)
        #self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
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
        self.t_tick = None
        self.__path = path
        if os.path.exists(path):
            os.remove(path)
        os.mkfifo(path)


    def close(self):
        os.remove(self.__path)
        os.remove(self.__image_pipe)


    def propagate(self,position,rotation,output):
        if len(position)>=3 and len(rotation)>=3:
            rotation *= 57.295779513
            session = open(self.__path,'w')
            session.write('%f %f %f %f %f %f\n' % (position[2],position[1],position[0],rotation[0],rotation[2],-rotation[1]))
            if output:
                print('%f %f %f %f %f %f' % (position[0],position[1],position[2],rotation[0],rotation[2],rotation[1]))
            session.close()
        else:
            raise Exception("Le format des sorties est incorrect")
