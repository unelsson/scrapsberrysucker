#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialread
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
  x = serialread.ser.readline()
  ##print(x)
  ch = read_ch()
  print(ch)
  if k==2490368:
    print("UP")
  if k==2424832:
    print('LEFT')
  if k==2555904:
    print('RIGHT')
  if k==2621440:
    print("DOWN")
  if k==27:  
    print('ESC')
  ## try:
  ##  x = int(x)
  ##  if int(x) >= 0 & int(x) <= 500:
  ##    for i in range(0, x, 25):
  ##      print ('#', end='')
  ##except ValueError:
  ##  print('Invalid read')
  ##  time.sleep(0.5)
  ##  os.system('clear')
  
