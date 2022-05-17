#!/usr/bin/python3

import sys,os
import curses
import time
import datetime
import csv
from collections import deque

class GUI:


    def __init__(self):
        self.s=curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.readouts=[]
        self.logtables=[]
        self.readWid = 30
        self.readX = 0

    def addReadout(self, value, label,unit="",group=""):
        self.readouts.append({"value":str(value),"label":label,"group":group,"unit":unit})
        return len(self.readouts)-1

    def updateReadout(self,index, value):
        self.readouts[index]["value"]=str(value)

    def addLogTable(self,headers,filepath,lines=None):
        headers.insert(0,"time                    ")
        self.logtables.append({"headers":headers,"lines":lines,"filepath":filepath})

        with open(filepath,"w") as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(headers)

        return len(self.logtables)-1

    def updateLogTable(self,index,data):
        data.insert(0,str(datetime.datetime.now()))
        with open(self.logtables[index]["filepath"],"a") as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(data)

    def getLogData(self, index,lines):
        data=[]
        with open(self.logtables[index]["filepath"]) as f:
            for line in deque(f, lines):
                data.append(list(csv.reader([line]))[0])
        return data

    

    def update(self):
        self.nextX = 0
        self.nextY = 1
        self.lastY = 0
        self.maxReadY = 0
        self.s.clear()
        self.s.refresh()
        height, width = self.s.getmaxyx() # get the window size
        self.s.addstr(0, 0, " " * width, curses.color_pair(2))
        self.s.addstr(0, 0, "Capacitor Reforming GP-IB Automation", curses.color_pair(2))

        wins={}
        for index , readout in enumerate(self.readouts):
            group=False
            if readout["group"] == "":
                winid=index
            else:
                winid=readout["group"]
                group=True

            # curses.newwin(height, width, begin_y, begin_x)
            if winid not in wins:
                wins[winid]={"win":curses.newwin(3, self.readWid, 1+self.nextY, 1+self.nextX),"values":1}
                self.nextX+=self.readWid
                
                if self.maxReadY < 3:
                    self.maxReadY = 3

                if self.nextX+self.readWid +2 > width:
                    self.nextX = 0
                    self.nextY += self.maxReadY
                    self.maxReadY = 0
            else:
                wins[winid]["values"]+=1
                
                if self.maxReadY < 2+wins[winid]["values"]:
                    self.maxReadY = 2+wins[winid]["values"]
                wins[winid]["win"].addstr(0+wins[winid]["values"],0," " * (self.readWid-1))
                wins[winid]["win"].resize(2+wins[winid]["values"],self.readWid)

            

            wins[winid]["win"].border(0)
            if group:
                wins[winid]["win"].addstr(0,2,readout["group"])
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout["label"])
                wins[winid]["win"].addstr(wins[winid]["values"],2+len(readout["label"]),": " +readout["value"]+readout["unit"])
            else:
                wins[winid]["win"].addstr(0,2,readout["label"])
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout["value"]+readout["unit"])

        # Reset position for next window group
        self.nextX = 0
        self.nextY += self.maxReadY+1
        
        tablespace=(height-self.nextY)/len(self.logtables)
        for index , logtable in enumerate(self.logtables):
            if logtable["lines"] is None:
                lines = int(tablespace)
            else:
                lines = logtable["lines"]

            i="log-"+str(index)
            wins[i]={"win":curses.newwin(lines, width-2, self.nextY, 1+self.nextX),"values":1}
            self.nextY += lines
            wins[i]["win"].border(0)
            tx=1
            ty=1
            wins[i]["win"].addstr(0,2,logtable["filepath"])
            
            for hindex , header in enumerate(logtable["headers"]):
                wins[i]["win"].addstr(ty,tx,header,curses.color_pair(2))
                wins[i]["win"].addstr(ty,tx+len(header),"|")
                tx+=len(header)+1

            tx=1
            ty=2
            
            for lindex , log in enumerate(self.getLogData(index,lines-3)):
                for dindex , data in enumerate(log):
                    wins[i]["win"].addstr(ty,tx,str(data))
                    wins[i]["win"].addstr(ty,tx+len(self.logtables[index]["headers"][dindex]),"|")
                    tx+=len(self.logtables[index]["headers"][dindex])+1
                ty+=1
                tx=1


        for index in wins:
            wins[index]["win"].refresh()

        self.s.refresh()


    def end(self):
        curses.endwin() # restore the terminal settings back to the original

