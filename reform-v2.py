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

gui.addReadout("12V","Voltage","PSU")
gui.addReadout("2mA","Current","PSU")
gui.addReadout("240uA","Current","DMM")

while(True):
    gui.update()
    time.sleep(5)

