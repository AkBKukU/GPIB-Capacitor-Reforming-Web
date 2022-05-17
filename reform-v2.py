#!/usr/bin/python3

import sys
import signal
import time
import random

from dmm import DMM34401A
from psu import PSU6633A
from gui import GUI

gui = GUI()
#psu = PSU6633A(7)
#dmm = DMM34401A(12)


# Handle Ctrl+C closes of program
def signal_handler(sig, frame):
    gui.end()
    # Add PSU output disable
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def getPSUVolts():
    return random.randint(5,12)

def getPSUCurrent():
    return random.randint(0,10)

def getDMMCurrent():
    return random.randint(0,20)


d={}
d["psu"]={}
d["dmm"]={}
d["r_limit"]={}
d["cap"]={}

d["psu"]["v"]=0
d["psu"]["i"]=0
d["dmm"]["i"]=0
d["r_limit"]["r"]=220
psu_v=12
psu_i=2
dmm_i=240

d["psu"]["v_id"]=gui.addReadout(psu_v,"Voltage","V","PSU")
d["psu"]["i_id"]=gui.addReadout(psu_i,"Current","mA","PSU")

d["dmm"]["v_id"]=gui.addReadout(dmm_i,"Current","uA","DMM")

d["cap"]["v_id"]=gui.addReadout(dmm_i,"Voltage","V","Capacitor")
d["cap"]["r_id"]=gui.addReadout(dmm_i,"Resistance","Ohms","Capacitor")


log_i=gui.addLogTable(["PSU Voltage","PSU Current","DMM Current","Cap Voltage", "Cap Resistance"],"test.csv")


while(True):

    # Get new instrument readings
    d["psu"]["v"]=getPSUVolts()
    d["psu"]["i"]=getPSUCurrent()
    d["dmm"]["i"]=getDMMCurrent()

    d["r_limit"]["v_drop"]=d["dmm"]["i"]*d["r_limit"]["r"]
    d["cap"]["v"]=d["psu"]["v"]-d["r_limit"]["v_drop"]
    
    try:
        d["cap"]["r"]=d["cap"]["v"]/d["dmm"]["i"]
    except ZeroDivisionError:
        d["cap"]["r"]=0


    gui.update()
    time.sleep(0.1)
    dmm_i+=5
    gui.updateReadout(d["psu"]["v_id"],d["psu"]["v"])
    gui.updateReadout(d["psu"]["i_id"],d["psu"]["i"])
    gui.updateReadout(d["dmm"]["v_id"],d["dmm"]["i"])
    gui.updateReadout(d["cap"]["v_id"],d["cap"]["v"])
    gui.updateReadout(d["cap"]["r_id"],str(d["cap"]["r"])[:6])
    gui.updateLogTable(log_i,[d["psu"]["v"],d["psu"]["i"],d["dmm"]["i"],d["cap"]["v"],d["cap"]["r"]])

