#!/usr/bin/python3

import sys
import signal
import time

from dmm import DMM34401A
from psu import PSU6633A
from gui import GUI

gui = GUI()

def signal_handler(sig, frame):
    gui.end()
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("import test")

psu_v=12
psu_i=2
dmm_i=240

gui.addReadout(psu_v,"Voltage","V","PSU")
gui.addReadout(psu_i,"Current","mA","PSU")
dmm_i_id=gui.addReadout(dmm_i,"Current","uA","DMM")

while(True):
    gui.update()
    time.sleep(5)
    dmm_i+=5
    gui.updateReadout(dmm_i_id,dmm_i)

