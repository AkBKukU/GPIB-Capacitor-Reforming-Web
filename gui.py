#!/usr/bin/python3

import sys,os
import curses
import time
import datetime
import csv
from collections import deque

class GUI:


    def __init__(self):
        # Initial screen and define settings for curses
        self.s=curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Data values to build displays for
        self.readouts=[]
        self.logtables=[]
        self.readWid = 30
        self.readX = 0
    
    # Add a readout window to the screen. Returns id for readout
    # Optional unit to postpend to value
    # Optional group to combine multiple readouts
    def addReadout(self, value, label,unit="",group=""):
        self.readouts.append({"value":str(value),"label":label,"group":group,"unit":unit})
        return len(self.readouts)-1

    # Update data for readout by id
    def updateReadout(self,index, value):
        self.readouts[index]["value"]=str(value)

    # Add a logging table window to the screen. Returns id for the readout
    # Optional lines to limit size of window
    def addLogTable(self,headers,filepath,lines=None):
        # Add time header with padded length for table
        headers.insert(0,"time                    ")
        self.logtables.append({"headers":headers,"lines":lines,"filepath":filepath})

        # Create logfile
        with open(filepath,"w") as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(headers)

        return len(self.logtables)-1

    # Update data for logging table
    def updateLogTable(self,index,data):
        # Add timestamp to data
        data.insert(0,str(datetime.datetime.now()))

        # Write line to logfile
        with open(self.logtables[index]["filepath"],"a") as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(data)

    # Gets last few lines from logfile as list
    def getLogData(self, index,lines):
        data=[]
        with open(self.logtables[index]["filepath"]) as f:
            for line in deque(f, lines):
                data.append(list(csv.reader([line]))[0])
        return data

    
    # Refresh and redraw GUI
    def update(self):
        # Positioning variables
        self.nextX = 0
        self.nextY = 1
        self.lastY = 0
        self.maxReadY = 0

        # Reset and redaw
        self.s.clear()
        self.s.refresh()
        height, width = self.s.getmaxyx() # get the window size

        # Header
        self.s.addstr(0, 0, " " * width, curses.color_pair(2))
        self.s.addstr(0, 0, "Capacitor Reforming GP-IB Automation", curses.color_pair(2))

        # Create all sub windows
        wins={}
        # Create readouts
        for index , readout in enumerate(self.readouts):
            # Check for a group and use that as the index 
            group=False
            if readout["group"] == "":
                winid=index
            else:
                winid=readout["group"]
                group=True

            # curses.newwin(height, width, begin_y, begin_x)
            # Create new window to use for display
            if winid not in wins:
                wins[winid]={"win":curses.newwin(3, self.readWid, 1+self.nextY, 1+self.nextX),"values":1}
                self.nextX+=self.readWid
                
                # Update position for next "line"
                if self.maxReadY < 3:
                    self.maxReadY = 3
                
                # Check if at the end of the window and drop to next "line"
                if self.nextX+self.readWid +2 > width:
                    self.nextX = 0
                    self.nextY += self.maxReadY
                    self.maxReadY = 0
            # Adding to existing group window
            else:
                # Update stored values for "line" positioning 
                wins[winid]["values"]+=1
                
                if self.maxReadY < 2+wins[winid]["values"]:
                    self.maxReadY = 2+wins[winid]["values"]

                # Clear bottom border
                wins[winid]["win"].addstr(0+wins[winid]["values"],0," " * (self.readWid-1))
                # Resize window before border is redrawn
                wins[winid]["win"].resize(2+wins[winid]["values"],self.readWid)


            # Draw border before text to add title
            wins[winid]["win"].border(0)
            if group:
                # Group as title
                wins[winid]["win"].addstr(0,2,readout["group"])
                # Label and value in window
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout["label"]+" : " +readout["value"]+readout["unit"])
            else:
                # Label as title
                wins[winid]["win"].addstr(0,2,readout["label"])
                # Value in window
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout["value"]+readout["unit"])

        # Reset position for next window group
        self.nextX = 0
        self.nextY += self.maxReadY+1
        
        # Determine height of dynamic tables
        tablespace=(height-self.nextY)/len(self.logtables)
        # Create all tables
        for index , logtable in enumerate(self.logtables):
            # Check iff table uses dynamic or static height
            if logtable["lines"] is None:
                lines = int(tablespace)
            else:
                lines = logtable["lines"]

            # Use log-# for window index
            i="log-"+str(index)
            # Create new window
            wins[i]={"win":curses.newwin(lines, width-2, self.nextY, 1+self.nextX),"values":1}
            # Draw border and use filename as title
            wins[i]["win"].border(0)
            wins[i]["win"].addstr(0,2,logtable["filepath"])
            # Update position
            self.nextY += lines

            # Begin position tracking in table
            tx=1
            ty=1
            
            # Print all headers
            for hindex , header in enumerate(logtable["headers"]):
                wins[i]["win"].addstr(ty,tx,header,curses.color_pair(2))
                wins[i]["win"].addstr(ty,tx+len(header),"|")
                tx+=len(header)+1

            # Update position
            tx=1
            ty=2
            
            # Get data from file and add to table
            for lindex , log in enumerate(self.getLogData(index,lines-3)):
                for dindex , data in enumerate(log):
                    # Print data and limit to length of header for fixed with
                    wins[i]["win"].addstr(ty,tx,str(data)[:len(self.logtables[index]["headers"][dindex])])
                    # Add deliniator
                    wins[i]["win"].addstr(ty,tx+len(self.logtables[index]["headers"][dindex]),"|")
                    # Update position for next data point
                    tx+=len(self.logtables[index]["headers"][dindex])+1

                # Update position for next line
                ty+=1
                tx=1

        # Draw all windows to buffer
        for index in wins:
            wins[index]["win"].refresh()

        # Draw to screen
        self.s.refresh()


    def end(self):
        curses.endwin() # restore the terminal settings back to the original

