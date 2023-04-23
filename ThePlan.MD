# The Plan**™** - **DONE**

## Control Landing Page - **DONE**

When the script page is first loaded present the following input options to the user to control the process of reforming

 - Maximum Capacitor Voltage
 - Current Limiting Resistor Value
 - Maximum Reforming Current
 - Minimum Reforming Current for next target Voltage
 - Log file name

## Data API - **DONE**

Use GET request from javascript client when accessing current data to provide timestamp of newest data that client has to know what new data created after timestamp to provide.

## Display Results

Realtime views in dedicated widgets for: 

 - All configured values from landing page - **DONE**
 - Target Voltage - **DONE**
 - Measured Current - **DONE**

Chart Following Values using https://leeoniya.github.io/uPlot/:  - **STARTED**

Voltage Chart: - **DONE**
 - Target Voltage - **DONE**
 - Measured Voltage - **DONE**

Voltage Chart Moving Window: - **DONE**
 - Same as previous voltage chart with limited data window for better views
 - Using `<input type=number>` to change data window size

Current Chart Moving Window: - **DONE**
 - Maximum Current
 - Measured Current
 - Minimum Current
 - Use same `<input type=number>` as voltage to change data window size

## Replay - **DONE**

Do not access GP-IB devices

Load existing CSV of data, generate new CSV in real, or accelerated, time using timestamps from previous CSV. Render web page to review data.

Have speed control as option when picking CSV to replay. speed control is number of lines to present with each new update request. fewer lines will be sub-realtime, more lines will be accelerated.

Setup page could have alternate menu for choosing from exiting files to both replay and download
