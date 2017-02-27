#!/usr/bin/python3
import os
import sys
import serialread
import time
import cv2
import numpy as np

while 1:
  x = serialread.ser.readline()
  print(x)
  k = cv2.waitKey(33)
  if k==2490368:
    print('UP')
  if k==2424832:
    print('LEFT')
  if k==2555904:
    print('RIGHT')
  if k==2621440:
    print('DOWN')
  time.sleep(1)
  ## try:
  ##  x = int(x)
  ##  if int(x) >= 0 & int(x) <= 500:
  ##    for i in range(0, x, 25):
  ##      print ('#', end='')
  ##except ValueError:
  ##  print('Invalid read')
  ##  time.sleep(0.5)
  ##  os.system('clear')
  
