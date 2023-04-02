# The Plan**™**

## Control Landing Page

When the script page is first loaded present the following input options to the user to control the process of reforming

 - Maximum Capacitor Voltage
 - Current Limiting Resistor Value
 - Maximum Reforming Current
 - Minimum Reforming Current for next target Voltage
 - Cycles (number of times to run full reform)

## Data API

Use GET request from javascript client when accessing current data to provide timestamp of newest data that client has to know what new data created after timestamp to provide.

## Display Results

Realtime views in dedicated widgets for: 

 - All configured values from landing page
 - Measured Voltage
 - Target Voltage
 - Measured Current

Chart Following Values using https://leeoniya.github.io/uPlot/:

Voltage Chart:
 - Maximum Capacitor Voltage
 - Target Voltage
 - Measured Voltage

Current Chart:
 - Maximum Current
 - Measured Current
 - Minimum Current

## Replay

Do not access GP-IB devices

Load existing CSV of data, generate new CSV in real, or accelerated, time using timestamps from previous CSV. Render web page to review data.
