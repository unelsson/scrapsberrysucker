#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np

def read_ch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

while 1:
  serread = serialrw.ser.readline()
  print("Non-decoded:", serread)
  print("Decoded", serread.decode('ascii'))
  ch = read_ch()
  print(ch)
  serialrw.ser.write(bytes(ch, 'ascii')); # Send pressed character to Arduino as bytes
  if ch=="q":  
    break
  if ch=="g": #Send IR scan command to Arduino
    try:
      for i in range(0, 19) #Receive values
        serread = serialrw.ser.readline()
        print(serread.decode('ascii'))
        j = int(serread)
        if j >= 0 & j <= 500:
          for i in range(0, j, 25):
            print('#', end='')
          print('')
      except ValueError:
        print('Invalid read')        
  
