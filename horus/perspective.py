#!/usr/bin/python

class TrapezeBuilder(object):

    def __init__(self,mask_builders):
        self.__mask_builders = mask_builders

    def show_trapeze(self,resolution):
        pass

    def build_trapeze(self,image):
        trapeze = {}

        _,_,a = mask_builders["a"].generate_mask(image)
        _,_,b = mask_builders["b"].generate_mask(image)
        _,_,c = mask_builders["c"].generate_mask(image)
        _,_,d = mask_builders["d"].generate_mask(image)

        ab = {}
        bc = {}
        cd = {}
        da = {}

        ab["derivative"] = (b[1]-a[1])/(b[0]-a[0])
        bc["derivative"] = (c[1]-b[1])/(c[0]-b[0])
        cd["derivative"] = (d[1]-c[1])/(d[0]-c[0])
        da["derivative"] = (a[1]-d[1])/(a[0]-d[0])
        ab["center"] = ((a[0]+b[0])/2,(a[1]+b[1])/2)
        bc["center"] = ((c[0]+b[0])/2,(c[1]+b[1])/2)
        cd["center"] = ((d[0]+c[0])/2,(d[1]+c[1])/2)
        da["center"] = ((a[0]+d[0])/2,(a[1]+d[1])/2)

        trapeze["a"] = a
        trapeze["b"] = b
        trapeze["c"] = c
        trapeze["d"] = d
        trapeze["ab"] = ab
        trapeze["bc"] = bc
        trapeze["cd"] = cd
        trapeze["da"] = da

        trapeze["origin"] = a
        if trapeze["origin"][0]>b[0]:
            trapeze["origin"] = b
        if trapeze["origin"][0]>c[0]:
            trapeze["origin"] = c
        if trapeze["origin"][0]>d[0]:
            trapeze["origin"] = d


        return trapeze

class DataCompiler(object):

    def __init__(self):
        pass

    def update_trapeze(self,trapeze):
        pass

    def get_distance(self,a,b):
        #distance = sqrt((focal*truewidth/mesured)^2+(board/2)^2)
        pass

    def get_roll(self):
        #Angle ROLL = arctan(bc["derivative"])
        pass

    def get_yaw(self):
        pass

    def get_pitch(self):
        pass

    def get_postion(self):
        #Find distance to 3 points, calculate equations and solve system
        pass
