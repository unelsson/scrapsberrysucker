#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np
import math
import urllib.request

serreaddata = ['/0']*19 #List for storing latest IR scan data
irdistdata = [0]*19 #Latest IR scan data converted to distances

mapsize = 100		#Map settings, robotx and roboty are map coordinates
#map = np.zeros((mapsize,mapsize)) #OLD MAP, 1 unit of map is 10cm
map = np.full((mapsize,mapsize,3), [100,100,100]); #Opencv2 img-type map greyscale
robotx = mapsize / 2
roboty = mapsize / 2
visionx = 0
visiony = 0
robotangle = 0.000
 
# This code was modified from pyimagesearch.com
# Test code for opening a snapshot to opencv2 from mjpg-streamer
resp = urllib.request.urlopen('http://127.0.0.1:8080/?action=snapshot" /')
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imwrite('camerass.jpg',image)

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
  print('X:', robotx, 'Y', roboty, 'Angle', robotangle)
  print(serreaddata)
  ch = read_ch()
  if ch=="w":
    serialrw.ser.write(b'w')
    robotx=robotx+math.sin(robotangle)*2 #Assuming 20cm movement
    roboty=roboty+math.cos(robotangle)*2
  if ch=="a":
    serialrw.ser.write(b'a')
    robotangle = robotangle - 0.52 #30 degrees of turn
  if ch=="s":
    serialrw.ser.write(b's')
    robotx=robotx-math.sin(robotangle)*1 #Assuming 10cm movement
    roboty=roboty-math.cos(robotangle)*1
  if ch=="d":
    serialrw.ser.write(b'd')
    robotangle = robotangle + 0.52 #30 degrees of turn
  if ch=="q":  
    break
  if ch=="g":
    serialrw.ser.write(b'g')
    time.sleep(2.5)
    try:
      for i in range(0, 19):
        serread = serialrw.ser.readline()
        serreaddata[i] = int(serread.decode('ascii').strip('\r\n'))
        if serreaddata[i] < 70: irdistdata[i]=10
        if serreaddata[i] <= 96 & serreaddata[i] > 70: irdistdata[i]=4
        if serreaddata[i] <= 120 & serreaddata[i] > 96: irdistdata[i]=3
        if serreaddata[i] <= 180 & serreaddata[i] > 120: irdistdata[i]=2
        if serreaddata[i] <= 235 & serreaddata[i] > 180: irdistdata[i]=2
        if serreaddata[i] <= 250 & serreaddata[i] > 235: irdistdata[i]=1
        if serreaddata[i] > 250: irdistdata[i]=1
        # Interpreting look() values (Sharp IR mean average)
        # 60-70 (free view, almost)
        #   96 (2 * A4 paper)
        #   120 (1,5 * A4 paper)
        #   180 (1 * A4 paper)
        #   235 (0,5 * A4 paper)
        if int(irdistdata[i]) > 0 & int(irdistdata[i]) < 6:
          visionx = round(robotx + math.sin(robotangle-1.57+i*0.174)*irdistdata[i])#This code does not yet take
          visiony = round(roboty + math.cos(robotangle-1.57+i*0.174)*irdistdata[i])#in account robotheading!
          if visionx > 0 & visionx < mapsize & visiony > 0 & visiony < mapsize:
            for k in range(0, irdistdata[i]+1):
              temporaryb = map[round(robotx+math.sin(robotangle-1.57+i*0.174)*k),round(roboty+math.cos(robotangle-1.57+i*0.174)*k),0]
              temporaryg = map[round(robotx+math.sin(robotangle-1.57+i*0.174)*k),round(roboty+math.cos(robotangle-1.57+i*0.174)*k),1]
              temporaryr = map[round(robotx+math.sin(robotangle-1.57+i*0.174)*k),round(roboty+math.cos(robotangle-1.57+i*0.174)*k),2]
              lightenedb = temporaryb + 70
              lightenedg = temporaryb + 70
              lightenedr = temporaryb + 70
              darkenedb = temporaryb - 70
              darkenedg = temporaryb - 70
              darkenedr = temporaryb - 70
              if lightenedb > 255: lightenedb = 255
              if lightenedg > 255: lightenedg = 255
              if lightenedr > 255: lightenedr = 255
              if darkenedb > 255: darkenedb = 255
              if darkenedg > 255: darkenedg = 255
              if darkenedr > 255: darkenedr = 255
              if lightenedb < 0: lightenedb = 0
              if lightenedg < 0: lightenedg = 0
              if lightenedr < 0: lightenedr = 0
              if darkenedb < 0: darkenedb = 0
              if darkenedg < 0: darkenedg = 0
              if darkenedr < 0: darkenedr = 0
              if k < irdistdata[i]: map[round(robotx+math.sin(robotangle-1.57+i*0.174)*k), round(roboty+math.cos(robotangle-1.57+i*0.174)*k)] = [darkenedb,darkenedg,darkenedr]
              if k == irdistdata[i]: map[visionx,visiony] = [lightenedb,lightenedg,lightenedr]
        cv2.imwrite('robomap.png', map)
    except ValueError:
      print('Invalid read')
  
