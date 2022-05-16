#!/usr/bin/python3

import sys
import time
import Gpib

## General GP-IB Setup ##
interface_id = 0 # Interface number of the GP-IB 
device_address = 7 # Address of the test insturment

device = Gpib.Gpib(interface_id,device_address) 

# write a command
#device.write("*IDN?") # Standard SCPI identification command
# read data back and print
#print(device.read(100)) # Read up to 100 bytes


## PSU Example ##
#volts = 13.37
current = 0.01
# Set voltage and current from python variable
#device.write("IOUT?")
#print(float(device.read(100)))
#device.write("ISET "+str(sys.argv[1]))

modes=["CONF:VOLT:DC 50,0.0005",
       "CONF:VOLT:AC 50,0.0005",
       "CONF:CURR:DC 50,0.0005",
       "CONF:CURR:AC 50,0.0005",
       "CONF:RES 50,0.0005",
       "CONF:FRES 50,0.0005",
       "CONF:FREQ 50,0.0005",
       "CONF:PER 50,0.0005",
       "CONF:CONT",
       "CONF:DIOD"]

## DMM Example ##
# set DC voltage for PSU range
for mode in modes:
    device.write(mode)
    print(mode)
    time.sleep(0.1)
    device.write("CONF?")
    print(device.read(100))

# read measurement back converted from scientific notation
#device.write("READ?")
#print(float(device.read(100)))
