#!/usr/bin/python3

import Gpib
import sys
import time

class PSU6633A:

    def __init__(self,gpib_address,gpib_interface=0):
        self.device = Gpib.Gpib(gpib_interface,gpib_address)
        
    def getOutput(self,value):
        self.device.write("OUT?")
        return float(self.device.read(100))
        
    def setOutput(self,value):
        self.device.write("OUT "+str(value))
        
    def setVolt(self, value):
        self.device.write("VSET "+str(value))

    def setCurrent(self, value):
        self.device.write("ISET "+str(value))
    
    def getVolt(self):
        self.device.write("VOUT?")
        return float(self.device.read(100))
    
    def getCurrent(self):
        self.device.write("IOUT?")
        return float(self.device.read(100))


