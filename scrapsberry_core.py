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
irdistdata = ['/0']*19 #Latest IR scan data converted to distances

mapsize = 100		#Map settings, robotx and roboty are map coordinates
#map = np.zeros((mapsize,mapsize)) #OLD MAP, 1 unit of map is 10cm
map = np.zeros((mapsize,mapsize,3), np.uint8); #Opencv2 img-type map greyscale
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
    robotx=robotx+math.sin(robotangle)*3 #Assuming 30cm movement
    roboty=roboty+math.cos(robotangle)*3
  if ch=="a":
    serialrw.ser.write(b'a')
    robotangle = robotangle - 0.09 #5 degrees of turn
  if ch=="s":
    serialrw.ser.write(b's')
    robotx=robotx-math.sin(robotangle)*3 #Assuming 10cm movement
    roboty=roboty-math.cos(robotangle)*3
  if ch=="d":
    serialrw.ser.write(b'd')
    robotangle = robotangle + 0.09 #5 degrees of turn
  if ch=="q":  
    break
  if ch=="g":
    serialrw.ser.write(b'g')
    time.sleep(2.5)
    try:
      for i in range(0, 19):
        serread = serialrw.ser.readline()
        serreaddata[i] = serread.decode('ascii').strip('\r\n')
        irdistdata[i] = -int(serreaddata[i])/100+6 #Convert str to int, sensordata -> distancedata
        if int(irdistdata[i]) > 0 & int(irdistdata[i]) < 6:
          visionx = round(robotx + math.sin(robotangle-i*0.174)*irdistdata[i])#This code does not yet take
          visiony = round(roboty + math.cos(robotangle-i*0.174)*irdistdata[i])#in account robotheading!
          print('DEBUG, we got this far!', visionx, visiony)
          if visionx > 0 & visionx < mapsize & visiony > 0 & visiony < mapsize:
            map[visionx,visiony] = [255,255,255]
            print('DEBUG, we got as far as we wanted!')
        cv2.imwrite('robomap.png', map)
    except ValueError:
      print('Invalid read')
  
