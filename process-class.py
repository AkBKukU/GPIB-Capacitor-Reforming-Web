#!/usr/bin/python3
from multiprocessing import Process, Value
import time

class Worker(Process):
    def __init__(self):
        self.spin=Value('i', 1)
        self.configured=Value('i', 0)
        self.data=Value('d', 0.0)
        Process.__init__(self)

    def run(self):
        while(self.spin.value):
            if(self.configured.value):
                self.data.value = float(time.time())
            time.sleep(0.1)

    def end(self):
        self.spin.value=False

    def startRunning(self):
        self.configured.value=1

    def read(self):
        return self.data.value

def main():
    dmm = Worker()
    dmm.start()
    for i in range(20):
        time.sleep(0.3)
        if i == 2:
            dmm.startRunning()
        if i == 15:
            dmm.end()
        print(i, dmm.read())

if __name__ == '__main__': main()
