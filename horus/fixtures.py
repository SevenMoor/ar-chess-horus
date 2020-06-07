#!/usr/bin/python

import numpy as np

class FixtureGenerator(object):

    def __init__(self,init_position,init_rotatation):
        self.__position = init_position
        self.__rotation = init_rotation
        self.__counter = 0

    def test_turn_around(self,point):
        pass

    def test_pitch(self):
        pass

    def test_yaw(self):
        pass

    def test_roll(self):
        pass

    def test_random_move(self):
        pass

    def run(self,test,point=(0,0,0)):
        pass
