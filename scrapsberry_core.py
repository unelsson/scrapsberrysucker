#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np
import atexit
from select import select

import sys
import select
import tty
import termios

class nbc(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False
   
def main():
  while 1:
    #ch = read_ch()
    ch = nbc.get_data()
    print(ch)
    serialrw.ser.write(bytes(ch, 'ascii')); # Send pressed character to Arduino as bytes
    if ch=="q":  
      break
    print(serialrw.ser.inWaiting())
    if serialrw.ser.inWaiting() > 18: 
      serialrw.ser.flush()
    if serialrw.ser.inWaiting() == 18:
      try:
        for i in range(0, 19): #Receive values
          serread = serialrw.ser.readline()
          print(serread.decode('ascii'))
          j = int(serread)
          #if j >= 0 & j <= 500:
          #for i in range(0, j, 25):
          #  print('#', end='')
          #print('')
      except ValueError:
        print('Invalid read')
        
main()
