# GPIB Capacitor Reforming with Web GUI  
*Non web version: [https://github.com/AkBKukU/GPIB-Capacitor-Reforming](https://github.com/AkBKukU/GPIB-Capacitor-Reforming)*

Controlling GP-IB test equipment to automate reforming capacitors with live data display


## Tested Hardware

- HP 6633A ([Manual](https://archive.org/details/hp-6632-a-33-a-34-a-operating)) - Programmable power supply with 0-50V, 0-2A range
- HP 34401A ([Manual](https://archive.org/details/manuallib-id-2600272)) - 6.5 digit multimeter
  
## Dependencies
 - Python3
 - [Linux-GPIB](https://sourceforge.net/projects/linux-gpib/) - GP-IB interface kernel driver
 - [Flask](https://flask.palletsprojects.com/en/2.2.x/) - Web interface server
 - [uPlot](https://github.com/leeoniya/uPlot) - JS plotting library

## Theory

Capcitors need to be slowly brought up to their rated voltage at a limited current (10m max per [this guide](https://web.archive.org/web/20220514225249/https://www.hb9aik.ch/notes/MIL-HDBK-1131C.pdf)). The goal is to rebuild the oxide layer acting as a dialectric that forms on the aluminum foil. Too much current or too high a voltage on a weakened capacitor will short through the dialectric causing catastrophic failure. The amount of oxide is relative to the maximum voltage the capacitor can handle.

## Software Usage

### GPIB Setup
The gpib kernel module needs to be rebuilt after kernel updates. After the standard `make` and  `make install`, remember to modprobe it:

```bash
modprobe ni_usb_gpib
```
  
### Setup Page
Run with `python3 reform-v2.py`. Will launch locally hosted web server likely accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000). The test may be configured using values for:  
 - Maximum voltage - Match to capacitor's rated voltage)  
 - Current limiting resistor - Used in series with capacitor to limit current
 - Minimum Current - Threshold to determine oxide rebuild is slowed  
 - Maximum Current - Used to calculate next voltage step to not exceed specified current  

There is also a section for downloading logs from previous tests and the option to re-display them through the live view page.

### Data View

This page shows live readings directly from test equipment and from calculations based on measurements. It also shows three live plots of the test results. These plots show the voltage changes and current draw of the capacitor. The overall voltage gets a single large plot with two small plots next to it showing just the recent samples for voltage and current. The number of samples to display is configurable in real time.

From the view page you make also end the reforming at any time.

You may leave the view page displayed in one browser window continuously and configure the parameters on the setup page in another or on different computers. When a new reform process is started the view page automatically refreshes to display new data. Any number of clients may view the live page at a any time.

## Method

Using the programmable power supply to automate this will allow the process to be more efficiently handled for larger quantities of capacitors.

The basic steps that need to be taken are as follows:
 1. Connect weak capacitor at zero voltage and current to PSU
 2. Increase voltage by a small percentage of maximum rated value, with current limited
 3. Watch current taken in by capacitor drop as capacitor reforms
 4. When current drops significantly it has been formed up to that voltage, go back to step 2.
 5. When the maximum voltage rating has been reached and current rating reduces the capacitor reforming is complete


## Interfacing

This software uses GP-IB interfacable EE test equipment to reform the capacitor and needs at minimum a meter capable of measuring uA of current and a power supply capable of delivering the voltage range of your capacitor. Different equipment will use different interface protocols, I have written the software to work with the hardware I have. You can easily modify the `dmm.py` and `psu.py` files to change the software to work with different test equipment.

### Power Supply - HP 6633A
The 6633A uses a unique GP-IB command format. The basic control commands:

 - `VSET #` : Sets the output voltage on the PSU
 - `ISET #` : Sets the current limit on the PSU
 - `OUT [0,1]` : Enables or disables the output
 - `VOUT?` : Returns the current voltage measured at the output
 - `IOUT?` : Returns the current amperage measured at the output

### Multi meter - HP 34401A
The 34401A uses SCPI for programming which is a robust standard with many options. The following are relevant to this project:

 - `CONF:VOLT:DC [range upper],[resolution minimum]` : Set DC voltage measurement mode and configure range setting
 - `CONF:RES [range upper],[resolution minimum]` : Set resistance measurement mode and configure range setting
 - `READ?` : Take a measurement and read it back
 - `SYST:BEEP` : Make short beep sound

