#!/usr/bin/python

import os
import re

class ConfigManager(object):

    def __init__(self, file):
        self.__file = open(file,"r+")
        self.__content = self.__file.readlines()

    def get(self,param_key):
        key_block = False
        pattern = re.compile("(\w+)=(\w+)")
        params = {}

        for line in self.__content:
            if key_block == True and line.strip().startswith("["):
                break

            if line.strip() == "["+param_key+"]":
                key_block = True

            if key_block == True and not line.strip().startswith("#"):
                if pattern.match(line):
                    s = re.search(pattern,line)
                    params[s.group(1)] = int(s.group(2))

        return params

    def set(self,block,param_key,value):
        key_block = False

        for i in range(len(self.__content)):
            line = self.__content[i]
            if line.strip().startswith("[") and key_block == True:
                break

            if line.strip() == "["+block+"]":
                key_block = True


            if key_block == True and line.strip().startswith(param_key+"="):
                self.__content[i] = param_key+"="+value+"\n"

        text = "".join([str(line) for line in self.__content])
        self.__file.seek(0)
        self.__file.write(text)

    def close(self):
        self.__file.close()
