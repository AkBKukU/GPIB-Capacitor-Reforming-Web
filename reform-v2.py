#!/usr/bin/python3

import sys, os, fnmatch, shutil
import signal
import time
import random
from ctypes import *

from multiprocessing import Process, Value, Array


from dmm import DMM34401A
from psu import PSU6633A
from gui import GUI

# Web landing page configurable values
web_cap_voltage = Value('d', 0.0)
web_resistor = Value('d', 220.0)
web_current_max = Value('d', 2000.0)
web_current_min = Value('d', 150.0)
web_log_name = Value(c_wchar_p,"Reform Log")



def reform():
    gui = GUI()
    psu = PSU6633A(12)
    dmm = DMM34401A(7)

    psu.setCurrent(0.01)
    psu.setVolt(1)

    dmm.setCurrent(0.01,0.000001)

    # Handle Ctrl+C closes of program
    def signal_handler(sig, frame):
        gui.end()
        # Add PSU output disable
        psu.setCurrent(0)
        psu.setVolt(0)
        print('You pressed Ctrl+C!')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    def getPSUVolts():
        return psu.getVolt()

    def getPSUCurrent():
        return psu.getCurrent()

    def getDMMCurrent():
        i=dmm.read()*1000000
        if i > 0:
            return i
        else:
            return 0


    d={}
    d["psu"]={}
    d["dmm"]={}
    d["r_limit"]={}
    d["cap"]={}
    d["calc"]={}

    d["psu"]["v"]=0
    d["psu"]["i"]=0
    d["dmm"]["i"]=0
    d["calc"]["v"] = 0


    d["calc"]["v_max"] = 16
    d["r_limit"]["r"]=220
    d["cap"]["i_max"]=2000 # Calculate next jump to 2mA
    d["cap"]["i_min"]=150 # Calculate next jump to 2mA


    # Garbage UI init data
    psu_v=12
    psu_i=2
    dmm_i=240

    d["psu"]["v_id"]=gui.addReadout(psu_v,"Voltage","V","PSU")
    d["psu"]["i_id"]=gui.addReadout(psu_i,"Current","mA","PSU")


    d["calc"]["v_id"]=gui.addReadout(dmm_i,"Target Voltage","V","Controls")
    d["calc"]["v_max_id"]=gui.addReadout(dmm_i,"Max Voltage","V","Controls")
    d["cap"]["i_max_id"]=gui.addReadout(dmm_i,"Max Current","uA","Controls")
    d["cap"]["i_min_id"]=gui.addReadout(dmm_i,"Min Current","uA","Controls")

    d["dmm"]["v_id"]=gui.addReadout(dmm_i,"Current","uA","DMM")

    d["cap"]["v_id"]=gui.addReadout(dmm_i,"Voltage","V","Capacitor")
    d["cap"]["r_id"]=gui.addReadout(dmm_i,"Resistance","Ohms","Capacitor")


    t = time.localtime()
    log_i=gui.addLogTable(["PSU Voltage","PSU Current","Target Voltage","DMM Current","Cap Voltage", "Cap Resistance"],time.strftime('%Y-%m-%d_%H-%M-%S', t)+"_"+str(web_log_name.value)+".csv")

    settle=10
    while(d["psu"]["v"] < d["calc"]["v_max"]):

        # Get new instrument readings
        d["psu"]["v"]=getPSUVolts()
        d["psu"]["i"]=getPSUCurrent()
        d["dmm"]["i"]=getDMMCurrent()

        d["r_limit"]["v_drop"]=(d["dmm"]["i"]/1000000)*d["r_limit"]["r"]
        d["cap"]["v"]=d["psu"]["v"]-d["r_limit"]["v_drop"]

        try:
            d["cap"]["r"]=d["cap"]["v"]/(d["dmm"]["i"]/1000000)
        except ZeroDivisionError:
            d["cap"]["r"]=0

        # Check for min current and calc voltage jump
        if d["dmm"]["i"] < d["cap"]["i_min"]:
            d["calc"]["v"] = d["cap"]["v"] + ((d["cap"]["i_max"]/1000000) * d["r_limit"]["r"])
            psu.setVolt(d["calc"]["v"])


        gui.update()
        time.sleep(0.1)
        dmm_i+=5
        gui.updateReadout(d["psu"]["v_id"],d["psu"]["v"])
        gui.updateReadout(d["psu"]["i_id"],d["psu"]["i"])
        gui.updateReadout(d["calc"]["v_id"],d["calc"]["v"])
        gui.updateReadout(d["calc"]["v_max_id"],d["calc"]["v_max"])
        gui.updateReadout(d["cap"]["i_max_id"],d["cap"]["i_max"])
        gui.updateReadout(d["cap"]["i_min_id"],d["cap"]["i_min"])
        gui.updateReadout(d["calc"]["v_id"],d["calc"]["v"])
        gui.updateReadout(d["dmm"]["v_id"],d["dmm"]["i"])
        gui.updateReadout(d["cap"]["v_id"],d["cap"]["v"])
        gui.updateReadout(d["cap"]["r_id"],str(d["cap"]["r"])[:6])
        gui.updateLogTable(log_i,[d["psu"]["v"],d["psu"]["i"],d["calc"]["v"],d["dmm"]["i"],d["cap"]["v"],d["cap"]["r"]])

        # Runaway current protection
        if d["dmm"]["i"] > 2*d["cap"]["i_max"]:
            if settle:
                settle-=1
            else:
                break



    psu.setCurrent(0)
    psu.setVolt(0)
    dmm.beep()


procs = []
proc = Process(target=reform)  # instantiating without any argument
procs.append(proc)
proc.start()

for proc in procs:
    proc.join()
