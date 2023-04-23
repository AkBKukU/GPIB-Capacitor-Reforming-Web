#!/usr/bin/python3

import sys, os, fnmatch, shutil
import signal
import time
import random
import datetime
from ctypes import *
import csv
import json
import glob

from flask import Flask
from flask import request
from flask import send_file
from flask import redirect
from flask import make_response

from multiprocessing import Process, Manager, Value, Array


from dmm import DMM34401A
from psu import PSU6633A
from gui import GUI
time_key = "time                    "
control = {}

# Web landing page configurable values
web_cap_voltage = Value('d', 0.0)
web_resistor = Value('d', 220.0)
web_current_max = Value('d', 2000.0)
web_current_min = Value('d', 150.0)
control_reform = Value('d', 0.0)
control_active = Value('d', 1)

log_directory="logs"



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

            d["calc"]["v_max"] = float(di["set_volts"])
            d["r_limit"]["r"] = float(di["set_res"])
            d["cap"]["i_max"] = float(di["set_imax"]) # Calculate next jump to 2mA
            d["cap"]["i_min"] = float(di["set_imin"]) # Calculate next jump to 2mA


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
            di["web_csv"] = log_directory+"/"+str(time.strftime('%Y-%m-%d_%H-%M-%S', t)+"_"+str(di["log_name"])+".csv")
            log_i=gui.addLogTable(["PSU Voltage","PSU Current","Target Voltage","DMM Current","Cap Voltage", "Cap Resistance"],di["web_csv"])

            settle=10
            while(d["psu"]["v"] < d["calc"]["v_max"] and control_reform.value):

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
                #time.sleep(0.1)
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
    d["web_csv"] = "logs/log.csv"
    d["log_name"] = "Reform Log"
    d["set_volts"] = "20"
    d["set_res"] = "220"
    d["set_imin"] = "150"
    d["set_imax"] = "2000"
    control["start_time"] = 0
    control["active"] = 0
    control["voltage"] = 0
    control["resistance"] = 0
    control["imin"] = 0
    control["imax"] = 0
    line_send = 0
    replay_file = None

    procs = []
    proc = Process(target=reform, args=(d,))  # instantiating without any argument
    procs.append(proc)

    proc.start()

    app = Flask("The Reform Script")

    @app.route("/")
    def start_reform():
    #web_csv.value = None

        #control_reform.value = 1

        if control_reform.value:
            return redirect("/view")
        else:
            return redirect("/setup")

    @app.route("/view")
    def web_view():
        global line_send
        global replay_file
        print("Viewing data")
        try:
            line_send = int(request.args.get("lines"))
        except:
            line_send=0

        try:
            replay_file = request.args.get("log_filename")
            print("Log file is: " + str(replay_file))
        except:
            return redirect("/setup?error=log_name")


        return send_file("static/html/view.html")

    @app.route("/setup",methods=["GET","POST"])
    def web_setup():
        if request.method == 'POST':
            try:
                d["set_volts"] = float(request.form.get("voltage"))
                control["voltage"] = d["set_volts"]
            except:
                return redirect("/setup?error=voltage")

            try:
                d["set_res"] = float(request.form.get("resistor"))
                control["resistance"] = d["set_res"]
            except:
                return redirect("/setup?error=resistor")
            try:
                d["set_imin"] = float(request.form.get("imin"))
                control["imin"] = d["set_imin"]
            except:
                return redirect("/setup?error=imin")
            try:
                d["set_imax"] = float(request.form.get("imax"))
                control["imax"] = d["set_imax"]
            except:
                return redirect("/setup?error=imax")
            try:
                d["log_name"] = request.form.get("log_name")
            except:
                return redirect("/setup?error=log_name")

            # TODO - Check values to prevent fire
            control_reform.value = 1
            return redirect("/view")

        return send_file("static/html/setup.html")

    @app.route("/kill")
    def kill():
        global line_send
        global replay_file

        line_send = 0
        replay_file = None
        control_reform.value = 0
        return send_file("static/html/kill.html")

    @app.route("/control.json")
    def control_json():
        control["active"] = control_reform.value
        return control


    @app.route("/logs.json")
    def logs_json():
        return list(map(lambda x: x.split('/',1)[1], sorted(glob.glob(log_directory+'/*.csv'), reverse=True)))

    @app.route("/logs_download")
    def logs_download():
        log_filename = 0
        try:
            log_filename = str(request.args.get("log_filename"))


            r = make_response(open(str(log_directory+"/"+log_filename)).read())
            r.headers['Content-type'] = "text/plain"
            r.headers['Content-disposition'] = "attachment; filename=\"" +log_filename+ "\""

            return r
        except:
            return redirect("/setup?error=log_name")

        return "File's not here, man",401

    @app.route("/data.json")
    def data_json():
        global line_send
        global replay_file
        time_get = str(request.args.get("time"))
        print("Opening CSV File: "+str(d["web_csv"]))
        print("GET time: "+str(time_get))

        if replay_file is None:
            filename = d["web_csv"]
        else:
            filename = log_directory+"/"+replay_file

        print("Log file is: " + str(filename))
        with open(str(filename)) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',')
            data = list(data)
            #data = (k.strip(), v.strip()) for k,v in data.items()
            data_new=[]
            new_point = -1
            for i,row in enumerate(data):
                row[time_key] = datetime.datetime.strptime(row[time_key], '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
                if (i == 0):
                    control["start_time"] = row[time_key]

                if row[time_key] == time_get:
                    new_point = i
                if new_point > -1 and new_point < i:
                    data_new.append(row)

            # Convert ISO8601 to Unix for uPlot
            #datetime.datetime.fromisoformat('2023-04-15 22:00:12.0004'.split(".")[0]).strftime('%s')
            if time_get == "None" or time_get == "0":
                return list(data[:(line_send if line_send else -1)])
            else:
                return list(data_new[:(line_send if line_send else -1)])


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
