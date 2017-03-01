#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np

serreaddata = ['/0']*19 #List for storing latest IR scan data
irdistdata = ['/0']*19 #Latest IR scan data converted to distances

mapsize = 100		#Map settings, robotx and roboty are map coordinates
map = np.zeros((mapsize,mapsize))
robotx = mapsize / 2
roboty = mapsize / 2

ch = 0

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
  print('You pressed',ch)
  print('Press W,A,S or D for movement, G for IR scan')
  print('Serial queue waiting (should be 0)', serialrw.ser.inWaiting())
  print(serreaddata)
  ch = read_ch()
  if ch=="w":
    serialrw.ser.write(b'w')
  if ch=="a":
    serialrw.ser.write(b'a')
  if ch=="s":
    serialrw.ser.write(b's')
  if ch=="d":
    serialrw.ser.write(b'd')
  if ch=="q":  
    break
  if ch=="g":
    serialrw.ser.write(b'g')
    time.sleep(2.5)
    try:
      for i in range(0, 19):
        serread = serialrw.ser.readline()
        serreaddata[i] = serread.decode('ascii').strip('\r\n')
        irdistdata[i] = int(serreaddata[i]) #This should be a conversion formula
        if i < 9 & irdistdata[i] > 100 :
          visionx = robotx - math.sin(i*10)*irdistdata[i]#This code does not yet take
          visiony = roboty - math.cos(i*10)*irdistdata[i]#in account robotheading!
          if visionx > 0 & visiony > 0 & visionx < mapsize & visiony < mapsize:
            map[visionx,visiony] = 2
    except ValueError:
      print('Invalid read')
  
