#!/usr/bin/python3

import Gpib
import sys
import time

class PSU6632A:

    def __init__(self,gpib_address,gpib_interface=0):
        device = Gpib.Gpib(gpib_interface_id,gpib_address)
        
    def getOutput(value):
        device.write("OUT?")
        return float(device.read(100))
        
    def setOutput(value):
        device.write("OUT  "+str(value))
        
    def setVolt(value):
        device.write("VOUT  "+str(value))

    def setCurrent(value):
        device.write("IOUT  "+str(value))
    
    def getVolt():
        device.write("VOUT?")
        return float(device.read(100))
    
    def getCurrent():
        device.write("IOUT?")
        return float(device.read(100))


