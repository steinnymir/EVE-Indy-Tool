# -*- coding: utf-8 -*-
"""
Created on Sun May 21 01:25:40 2017

@author: Stymir
"""

import time

#%% Utilities
    
class Timer(object):
    ''' '''
    def __init__(self):
        self.timestamps = []

    def tic(self):
        self.timestamps.append(time.time())

    def toc(self, out = 'print'):

        t = time.time()
        dt = (t - self.timestamps[-1]) * 1000
        self.timestamps.append(time.time())
        if out == 'return':
            return dt
        elif out == 'print':
            print('this took {0:3F} ms'.format(dt))

    def toc_end (self):
        self.timestamps.append(time.time())
        n=1
        t_prec= 0
        skip = True
        for t in self.timestamps:
            if not skip:
                dt =  (t - t_prec) * 1000
                t_prec = t
                print('time section {0}: {1:.3f} ms'.format(n,dt))
                n =+ 1
                
            else:
                t_prec = t
                skip=False
    def reset(self):
        self.timestamps = []

class Style:
    B_start = '\033[1m'
    B_stop = '\033[0m'

#%% Functions

def getNum_or_Str(string):
    ''' returns the correct format for input string'''
    try:
        out = int(string)
    except ValueError:
        try:
            out = float(string)
        except ValueError:
            out = string
    finally:
        return(out)

def roundup(number):
    if (number % 1)*10 >= 5:
        out = round(number)
    elif (number % 1)*10 == 0:
        out = round(number)
    else:
        out = round(number) + 1
    return out


def isk(num, suffix=' ISK'):
    for unit in ['','K','M']:
        if abs(num) < 1000.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'B', suffix)