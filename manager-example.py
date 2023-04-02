from multiprocessing import Process, Manager, Value
import json
import copy
import time
 
def f(d):
    for i in range(100):
        x = {}
        x[i] = f'hi {i}'
        d['res'] = x
        time.sleep(0.2)
 
if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
 
        p = Process(target=f, args=(d,))
        p.start()
 
        for i in range(100):
            print(i, d)
            time.sleep(0.2)
 
        p.join()
        print(d)