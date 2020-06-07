#!/usr/bin/python

import numpy as np
import math

class FixtureGenerator(object):

    def __init__(self,init_position,init_rotatation):
        self.__position = init_position
        self.__rotation = init_rotation
        self.__counter = 0
        self.__angle = 0
        self.__way_factor = 1

    def test_turn_around(self,point):
        self.__angle += 0.5
        self.__angle %= 360
        self.__position[0] = math.cos(self.__angle*math.pi/180) + point[0]
        self.__position[1] = point[1] + 95
        self.__position[2] = math.sin(self.__angle*math.pi/180) + point[2]
        self.__rotation[0] = -45
        self.__rotation[1] = -1 * self.__angle
        self.__rotation[2] = 0

        return self.__position, self.__rotation

    def test_pitch(self):
        self.__rotation[0] += 0.5
        self.__rotation[0] %= 360
        return self.__rotation

    def test_yaw(self):
        self.__rotation[1] += 0.5
        self.__rotation[1] %= 360
        return self.__rotation

    def test_roll(self):
        self.__rotation[2] += 0.5
        self.__rotation[2] %= 360
        return self.__rotation

    def test_translate_x(self):
        self.__position[0] += self.__way_factor
        self.__counter += 1
        if self.__counter > 95:
            self.__way_factor *= -1
            self.__counter = 0
        return self.__position

    def test_translate_y(self):
        self.__position[1] += self.__way_factor
        self.__counter += 1
        if self.__counter > 95:
            self.__way_factor *= -1
            self.__counter = 0
        return self.__position

    def test_translate_z(self):
        self.__position[2] += self.__way_factor
        self.__counter += 1
        if self.__counter > 95:
            self.__way_factor *= -1
            self.__counter = 0
        return self.__position

    def run(self,test,point=(0,0,0)):
        if test == "rotate_x":
            return self.__position, self.test_pitch()
        elif test == "rotate_y":
            return self.__position, self.test_yaw()
        elif test == "rotate_z":
            return self.__position, self.test_roll()
        elif test == "translate_x":
            return self.test_translate_x(), self.__rotation
        elif test == "translate_y":
            return self.test_translate_y(), self.__rotation
        elif test == "translate_z":
            return self.test_translate_z(), self.__rotation
        elif test == "circle_around":
            return test_turn_around(point)
        else:
            raise Exception("Nom de test invalide")
            return None
