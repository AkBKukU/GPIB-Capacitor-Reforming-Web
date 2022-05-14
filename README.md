# GPIB-Capacitor-Reforming
Controlling GPIB test equipment to automate reforming capacitors

## Hardware
- HP 6633A ([Manual](https://archive.org/details/hp-6632-a-33-a-34-a-operating)) - Programmable power supply with 0-50V, 0-2A range
- HP 34401A ([Manual](https://archive.org/details/manuallib-id-2600272)) - 6.5 digit multimeter

## Theory
Capcitors need to be slowly brought up to their rated voltage at a limited current (10m max per [this guide](https://web.archive.org/web/20220514225249/https://www.hb9aik.ch/notes/MIL-HDBK-1131C.pdf)). The goal is to rebuild the oxide layer acting as a dialectric that forms on the aluminium foil. Too much current or too high a voltage on a weakened capacitor will short through the dialectric causing catestrophic failure. The amount of oxide is relative to the maximum voltage the capacitor can handle

Using the programmable power supply to automate this will allow the process to be more efficiently handled for larger quantities of capacitors.

The basic steps that need to be taken are as follows:
 1. Connect weak capctitor at zero voltage and current to PSU
 2. Increase voltage by a small percentage of maximum rated value, with current limited
 3. Watch current taken in by capacitor drop as capacitor reforms
 4. When current drops significantly it has been formed up to that voltage, go back to step 2.
 5. When the maximum volage rating has been reached and current rating reduces the capacitor reforming is complete

