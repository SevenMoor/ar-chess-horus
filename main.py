#!/usr/bin/python
#coding: utf-8

import cv2
import argparse
import signal

from horus.io import *
from horus.vision import *
from horus.perspective import *
from horus.config import *
from horus.fixtures import *
from time import sleep

#=================
#Argument Handling
parser = argparse.ArgumentParser()
parser.add_argument("-o","--output",help="Affiche les positions calculées dans la console",action="store_true")
parser.add_argument("-p","--pipe",help="Chemin du pipe de communication à créer/ouvrir",default="/tmp/archess-cli")
parser.add_argument("-w","--webcam",help="Identifiant de la webcam à utiliser",default=0,type=int)
parser.add_argument("-c","--calibrate",help="Ouvre le programme avec le GUI de calibration du marqueur souhaité",choices=['a','b','c','d'])
parser.add_argument("-i","--integration-test",help="Indique de transmettre des données factices pour tester l'intégration spécifié",choices=['translate_x','translate_y','translate_z','rotate_x','rotate_y','rotate_z','circle_around'])
#A gérer
parser.add_argument("-t","--trapeze",help="Affiche dans une fenêtre le trapèze de perspective capturé",action="store_true")
parser.add_argument("-f","--focal",help="Configure et utilise la valeur fournie comme focale de la caméra en mm",default=50,type=int)
parser.add_argument("-b","--board",help="Configure et utilise la valeur fournie comme taille du plateau en mm",default=186,type=int)
args = parser.parse_args()



#======================
#Program Initialization
input = InputManager(args.webcam)
output = OutputManager(args.pipe)
config = ConfigManager("horus.cfg")

#Killing handler Definition
def kill_handler(signal,frame):
    output.close()
    input.close()
    config.close()

#Assigning Handlers
signal.signal(signal.SIGINT,kill_handler)
signal.signal(signal.SIGTERM,kill_handler)

if args.integration_test is not None:
    board = config.get("board")
    fix = FixtureGenerator([board["size"]/2,95,-board["size"]],[0,0,0])

    while True:
        position,rotation = fix.run(args.integration_test,[board["size"]/2,0,board["size"]/2])
        if args.output:
            print('%f %f %f %f %f %f' % (position[0],position[1],position[2],rotation[0],rotation[1],rotation[2]))
        output.propagate(position,rotation)
        sleep(0.03)
else:
    #=================
    #Mask Declarations
    a = config.get("a")
    b = config.get("b")
    c = config.get("c")
    d = config.get("d")

    mask_builders = {}

    mask_builders["a"] = ColorMaskBuilder(
        [a["h"],a["s"],a["v"]],
        {
            "hue-tolerance": a["ht"],
            "saturation-tolerance": a["st"],
            "value-tolerance": a["vt"]
        })

    mask_builders["b"] = ColorMaskBuilder(
        [b["h"],b["s"],b["v"]],
        {
            "hue-tolerance": b["ht"],
            "saturation-tolerance": b["st"],
            "value-tolerance": b["vt"]
        })

    mask_builders["c"] = ColorMaskBuilder(
        [c["h"],c["s"],c["v"]],
        {
            "hue-tolerance": c["ht"],
            "saturation-tolerance": c["st"],
            "value-tolerance": c["vt"]
        })

    mask_builders["d"] = ColorMaskBuilder(
        [d["h"],d["s"],d["v"]],
        {
            "hue-tolerance": d["ht"],
            "saturation-tolerance": d["st"],
            "value-tolerance": d["vt"]
        })



    #===================
    #Controls Definition
    if args.calibrate is not None:
        values = config.get(args.calibrate)

        def nothing(x):
            pass

        cv2.namedWindow("Controls")
        cv2.createTrackbar("h","Controls",values["h"],179,nothing)
        cv2.createTrackbar("s","Controls",values["s"],255,nothing)
        cv2.createTrackbar("v","Controls",values["v"],255,nothing)
        cv2.createTrackbar("ht","Controls",values["ht"],179,nothing)
        cv2.createTrackbar("st","Controls",values["st"],255,nothing)
        cv2.createTrackbar("vt","Controls",values["vt"],255,nothing)



    #=========
    #Main Loop
    while True:
        image = input.propagate()

        #-------------------------------
        #Update values based on controls
        if args.calibrate is not None:
            mask_builders[args.calibrate].update_parameters(
                [
                    cv2.getTrackbarPos("h","Controls"),
                    cv2.getTrackbarPos("s","Controls"),
                    cv2.getTrackbarPos("v","Controls")
                ]
                ,{
                    "hue-tolerance":cv2.getTrackbarPos("ht","Controls"),
                    "saturation-tolerance":cv2.getTrackbarPos("st","Controls"),
                    "value-tolerance":cv2.getTrackbarPos("vt","Controls")
                })

            #--------------
            #Key Operations
            mask,contours,_ = mask_builders[args.calibrate].generate_mask(image)

            scale_percent = 40 # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image

            #---------------------
            #Print relevant frames
            cv2.imshow("Image",cv2.cvtColor(cv2.resize(image, dim, interpolation = cv2.INTER_AREA),cv2.COLOR_HSV2BGR))
            cv2.imshow("Mask",cv2.resize(mask, dim, interpolation = cv2.INTER_AREA))
            cv2.imshow("Contours",cv2.resize(contours, dim, interpolation = cv2.INTER_AREA))

        if args.trapeze:
            cv2.imshow("Trapeze",trapeze_builder.show_trapeze((camera["width"],camera["height"])))

        #---------------
        #Event handling
        c = cv2.waitKey(1)
        if c == ord('q'):
            break
        elif c == ord("s") and args.calibrate is not None:
            config.set(args.calibrate,"h",cv2.getTrackbarPos("h","Controls"))
            config.set(args.calibrate,"s",cv2.getTrackbarPos("s","Controls"))
            config.set(args.calibrate,"v",cv2.getTrackbarPos("v","Controls"))
            config.set(args.calibrate,"ht",cv2.getTrackbarPos("ht","Controls"))
            config.set(args.calibrate,"st",cv2.getTrackbarPos("st","Controls"))
            config.set(args.calibrate,"vt",cv2.getTrackbarPos("vt","Controls"))



#========
#Cleaning
input.close()
output.close()
config.close()
cv2.destroyAllWindows()
