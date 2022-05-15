#!/bin/bash

./read-amps.py > volts.txt && scp volts.txt 192.168.12.216:/media/akbkuku/A068/
