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
  x = serialrw.ser.readline()
  print("Non-decoded:", x)
  print("Decoded", x.decode('ascii'))
  ch = read_ch()
  print(ch)
  serialrw.ser.write(bytes(ch, 'ascii')); # Send pressed character to Arduino as bytes
  if ch=="q":  
    break
  if ch=="g":
    try:
      x = serialrw.ser.readline()
      x = int(x)
      if int(x) >= 0 & int(x) <= 500:
        print(x.decode('ascii'))
        for i in range(0, x, 25):
          print ('#', end='')
    except ValueError:
      print('Invalid read')
      time.sleep(0.5)
  
