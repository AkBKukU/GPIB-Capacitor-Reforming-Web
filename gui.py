#!/usr/bin/python3

import sys,os
import curses
import time

class GUI:


    def __init__(self):
        self.s=curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.readouts=[]
        self.readWid = 30
        self.readX = 0

    def addReadout(self, value, label,group=""):
        self.readouts.append([value,label,group])

    def update(self):
        self.readX = 0
        self.s.clear()
        self.s.refresh()
        height, width = self.s.getmaxyx() # get the window size
        self.s.addstr(0, 0, " " * width, curses.color_pair(1))
        self.s.addstr(0, 0, "Test GUI", curses.color_pair(1))

        wins={}
        for index , readout in enumerate(self.readouts):
            group=False
            if readout[2] == "":
                winid=index
            else:
                winid=readout[2]
                group=True

            # curses.newwin(height, width, begin_y, begin_x)
            if winid not in wins:
                wins[winid]={"win":curses.newwin(3, self.readWid, 3, 1+(self.readX*self.readWid)),"values":1}
                self.readX+=1
            else:
                wins[winid]["values"]+=1
                wins[winid]["win"].addstr(0+wins[winid]["values"],0," " * (self.readWid-1))
                wins[winid]["win"].resize(2+wins[winid]["values"],self.readWid)

            

            wins[winid]["win"].border(0)
            if group:
                wins[winid]["win"].addstr(0,2,readout[2])
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout[1])
                wins[winid]["win"].addstr(wins[winid]["values"],2+len(readout[1]),": " +readout[0])
            else:
                wins[winid]["win"].addstr(0,2,readout[1])
                wins[winid]["win"].addstr(wins[winid]["values"],1,readout[0])
            

        for index in wins:
            wins[index]["win"].refresh()

        self.s.refresh()


    def end(self):
        curses.endwin() # restore the terminal settings back to the original

