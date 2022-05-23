#!/usr/bin/python3

import Gpib
import sys
import time

class DMM34401A:

    def __init__(self,gpib_address,gpib_interface=0):
        self.device = Gpib.Gpib(gpib_interface,gpib_address)
        self.modes = {
            "VOLTDC" : "VOLT",
            "VOLTAC" : "VOLT:AC",
            "CURRDC" : "CURR",
            "CURRAC" : "CURR:AC",
            "RES"    : "RES",
            "FRES"   : "FRES",
            "FREQ"   : "FREQ",
            "CONT"   : "CONT",
            "DIOD"   : "DIOD"
            }
    
    def getMode(self):
        self.device.write("CONF?")
        return str(self.device.read(100))

    def readVoltDC(self):
        if not self.getMode().startswith(self.modes["VOLTDC"]):
            return -1
        return self.read()

    def readCurrDC(self):
        if not self.getMode().startswith(self.modes["CURRDC"]):
            return -1
        return self.read()
        
    def setVolt(self, max_range, resolution):
        self.device.write("CONF:VOLT:DC "+str(max_range)+","+str(resolution))

    def setCurrent(self, max_range, resolution):
        self.device.write("CONF:CURR:DC "+str(max_range)+","+str(resolution))
    
    def read(self):
        self.device.write("READ?")
        return float(self.device.read(100))

    def beep(self):
        self.device.write("SYST:BEEP")


