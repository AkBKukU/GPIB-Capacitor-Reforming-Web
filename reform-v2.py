#!/usr/bin/python3

import sys, os, fnmatch, shutil
import signal
import time
import random
from ctypes import *
import csv
import json

from flask import Flask
from flask import request

from multiprocessing import Process, Manager, Value, Array


from dmm import DMM34401A
from psu import PSU6633A
from gui import GUI


# Web landing page configurable values
web_cap_voltage = Value('d', 0.0)
web_resistor = Value('d', 220.0)
web_current_max = Value('d', 2000.0)
web_current_min = Value('d', 150.0)
control_reform = Value('d', 0.0)
control_active = Value('d', 1)



def reform(di):
    while(control_active.value):
        time.sleep(0.5)
        print("acvtive")
        while (control_reform.value):
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
            di["web_csv"] = str(time.strftime('%Y-%m-%d_%H-%M-%S', t)+"_"+str(di["log_name"])+".csv")
            log_i=gui.addLogTable(["PSU Voltage","PSU Current","Target Voltage","DMM Current","Cap Voltage", "Cap Resistance"],di["web_csv"])

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
            gui.end()
            dmm.beep()
            control_reform.value = 0



with Manager() as manager:
    d = manager.dict()
    d["web_csv"] = "log.csv"
    d["log_name"] = "Reform Log"

    procs = []
    proc = Process(target=reform, args=(d,))  # instantiating without any argument
    procs.append(proc)

    proc.start()

    app = Flask("The Reform Script")

    @app.route("/")
    def start_reform():
    #web_csv.value = None

        control_reform.value = 1
        return " <p>Reform started</p>"

    @app.route("/kill")
    def kill():

        control_active.value = 0
        control_reform.value = 0
        return " <p>killing process</p>"

    @app.route("/data.json")
    def data_json():
        time_get = str(request.args.get("time"))
        print("Opening CSV File: "+str(d["web_csv"]))
        print("GET time: "+str(time_get))
        with open(str(d["web_csv"])) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',')
            data = list(data)
            data_new=[]
            new_point = None
            for i,row in enumerate(data):
                if row["time                    "] == time_get:
                    new_point = i
                if new_point is not None and new_point < i:
                    data_new.append(row)

            if time_get == "None":
                return list(data)
            else:
                return list(data_new)


    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r


    app.run(host="0.0.0.0")

    control_active.value = 0

    for proc in procs:
        proc.join()
