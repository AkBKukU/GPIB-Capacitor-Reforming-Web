#!/usr/bin/python3

import sys
import Gpib

cap_v_max=45
cap_i_max=0.003
cap_i_min=0.000045
r_limit=218 # 220 value measured at 218
step_low=0.01

psu_i_now=0.0
psu_v_now=0.0
cap_v=0
cap_i_nowc=0.0
cap_rpsu=0 # calculated
cap_rcalc=0 # calculated


## General GP-IB Setup ##
interface_id = 0 # Interface number of the GP-IB 
dmm_address = 7 # Address of the test insturment
psu_address = 12 # Address of the test insturment

dmm = Gpib.Gpib(interface_id,dmm_address) 
psu = Gpib.Gpib(interface_id,psu_address) 


# Base Setup
dmm.write("CONF:VOLT:DC 50,0.0005")
psu.write("VSET 0") # Will be adjusted as program runs
psu.write("ISET 0.01") # Fixed max value for protection

print("cap_v \t cap_i_nowc \t cap_rpsu \t cap_rcalc \t psu_v_now \t psu_i_now")

while (cap_v < cap_v_max):
    # Get current readings
    dmm.write("READ?")
    cap_v = float(dmm.read(100))

    psu.write("IOUT?")
    psu_i_now = float(psu.read(100))
    psu.write("VOUT?")
    psu_v_now = float(psu.read(100))
    cap_i_nowc = (psu_v_now - cap_v)/r_limit # preferred value

    cap_rpsu = cap_v / psu_i_now
    cap_rcalc = cap_v / cap_i_nowc

   
    # get target voltage
    target_v = cap_v + (cap_i_max*r_limit)
    
    # Check if target is higher than max
    #if (target_volts > volt_max):
    #    print ("Max Voltage Reached")
    #    break
    d="\t"
    # set psu voltage
    print(str(cap_v)+d+ str(cap_i_nowc)+d+ str(cap_rpsu)+d+ str(cap_rcalc)+d+ str(psu_v_now)+d+ str(psu_i_now))

    if(cap_i_nowc < cap_i_min):
        psu.write("VSET "+str(target_v)) # Will be adjusted as program runs

dmm.write("SYST:BEEP")
psu.write("VSET 0") # Will be adjusted as program runs
psu.write("ISET 0") # Fixed max value for protection
