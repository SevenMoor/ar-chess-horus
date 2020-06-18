#!/usr/bin/python

import math
import numpy as np
import cv2

class TrapezeBuilder(object):

    def __init__(self,mask_builders):
        self.__mask_builders = mask_builders
        self.__trapeze = None

    def show_trapeze(self,resolution):
        image = np.zeros((resolution[0],resolution[1],3))

        if self.__trapeze is not None:
            if self.__trapeze["a"] is not None and self.__trapeze["b"] is not None and self.__trapeze["c"] and self.__trapeze["d"] is not None:
                if self.__trapeze["a"][0] is not None and self.__trapeze["a"][1] is not None and self.__trapeze["b"][0] is not None and self.__trapeze["b"][1] is not None and self.__trapeze["c"][0] is not None and self.__trapeze["c"][1] is not None and self.__trapeze["d"][0] is not None and self.__trapeze["d"][1] is not None:
                    cv2.line(image,self.__trapeze["a"],self.__trapeze["b"],(255,255,255),2)
                    cv2.line(image,self.__trapeze["b"],self.__trapeze["c"],(255,255,255),2)
                    cv2.line(image,self.__trapeze["c"],self.__trapeze["d"],(255,255,255),2)
                    cv2.line(image,self.__trapeze["d"],self.__trapeze["a"],(255,255,255),2)

        return image

    def fake_trapeze(self,a,b,c,d):
        trapeze = {}

        trapeze["a"] = a
        trapeze["b"] = b
        trapeze["c"] = c
        trapeze["d"] = d

        self.__trapeze = trapeze

        return trapeze

    def build_trapeze(self,image):
        trapeze = {}

        _,conta,a = self.__mask_builders["a"].generate_mask(image)
        _,contb,b = self.__mask_builders["b"].generate_mask(image)
        _,contc,c = self.__mask_builders["c"].generate_mask(image)
        _,contd,d = self.__mask_builders["d"].generate_mask(image)

        trapeze["a"] = a
        trapeze["b"] = b
        trapeze["c"] = c
        trapeze["d"] = d

        self.__trapeze = trapeze

        return trapeze

class DataCompiler(object):

    def __init__(self,config):
        self.__trapeze = None
        self.__config = config

        board = self.__config.get("board")
        camera = self.__config.get("camera")

        self.__board_points = np.array([
            (0,0,0),
            (board["size"],0,0),
            (board["size"],0,board["size"]),
            (0,0,board["size"])
        ],dtype="double")

        self.__camera_matrix = np.array([
            [camera["focal"],0,camera["cx"]],
            [0,camera["focal"],camera["cy"]],
            [0,0,1]
        ],dtype="double")
        self.__dist_coeffs = np.zeros((4,1))

    def update_trapeze(self,trapeze):
        self.__trapeze = trapeze

    def get_board_pose(self):
        if self.__trapeze["a"][0] is not None and self.__trapeze["a"][1] is not None and self.__trapeze["b"][0] is not None and self.__trapeze["b"][1] is not None and self.__trapeze["c"][0] is not None and self.__trapeze["c"][1] is not None and self.__trapeze["d"][0] is not None and self.__trapeze["d"][1] is not None:
            projected_points = np.array([
                (self.__trapeze["a"][0],self.__trapeze["a"][1]),
                (self.__trapeze["b"][0],self.__trapeze["b"][1]),
                (self.__trapeze["c"][0],self.__trapeze["c"][1]),
                (self.__trapeze["d"][0],self.__trapeze["d"][1])
            ],dtype="double")

            success, rvector, tvector = cv2.solvePnP(self.__board_points, projected_points, self.__camera_matrix, self.__dist_coeffs,flags=cv2.SOLVEPNP_ITERATIVE)

            if success:
                return rvector, tvector
            else:
                return None, None
        else:
            return None, None


    def get_camera_pose(self,rvec,tvec):
        r_mat = cv2.Rodrigues(rvec)
        rt_mat = np.transpose(r_mat[0])
        cam_pos = -1 * rt_mat.dot(tvec)
        cam_rot_temporary = rt_mat.dot(np.array([
            0,
            0,
            1
        ]))

        #cam_rot = [cam_rot_temporary[0],0.0,cam_rot_temporary[2]]

        x_axis = r_mat[0].dot([1,0,0])
        z_axis = r_mat[0].dot([0,0,1])
        y_axis = np.cross(x_axis,z_axis)

        calculated_rotation = np.array([
            [x_axis],
            [y_axis],
            [z_axis]
        ])

        calculated_axises = np.transpose(calculated_rotation)
        cam_rot = calculated_axises.dot(np.array([
            0,
            0,
            1
        ]))

        return cam_pos, cam_rot

    def show_axis(self,image,rotation,translation):
        zero_axis, zero_jacobian = cv2.projectPoints(np.array([(0.0, 0.0, 0.0)],dtype="double"), rotation, translation, self.__camera_matrix, self.__dist_coeffs)
        x_axis, x_jacobian = cv2.projectPoints(np.array([(100.0, 0.0, 0.0)],dtype="double"), rotation, translation, self.__camera_matrix, self.__dist_coeffs)
        y_axis, y_jacobian = cv2.projectPoints(np.array([(0.0, 100.0, 0.0)],dtype="double"), rotation, translation, self.__camera_matrix, self.__dist_coeffs)
        z_axis, z_jacobian = cv2.projectPoints(np.array([(0.0, 0.0, 100.0)],dtype="double"), rotation, translation, self.__camera_matrix, self.__dist_coeffs)

        p_0 = (int(zero_axis[0][0][0]), int(zero_axis[0][0][1]))
        p_x = (int(x_axis[0][0][0]), int(x_axis[0][0][1]))
        p_y = (int(y_axis[0][0][0]), int(y_axis[0][0][1]))
        p_z = (int(z_axis[0][0][0]), int(z_axis[0][0][1]))

        cv2.line(image,p_0,p_x,(0,0,255),3)
        cv2.line(image,p_0,p_y,(0,255,0),3)
        cv2.line(image,p_0,p_z,(255,0,0),3)

        return image
