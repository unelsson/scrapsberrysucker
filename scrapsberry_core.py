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
  ##print(x)
  ch = read_ch()
  print(ch)
  if ch=="w":
    print("Pressed w")
    serialrw.ser.write('1')
  if ch=="a":
    print("Pressed a")
    serialrw.ser.write('2')
  if ch=="s":
    print("Pressed s")
    serialrw.ser.write('3')
  if ch=="d":
    print("Pressed d")
    serialrw.ser.write('4')
  if ch=="q":  
    break
  ## try:
  ##  x = int(x)
  ##  if int(x) >= 0 & int(x) <= 500:
  ##    for i in range(0, x, 25):
  ##      print ('#', end='')
  ##except ValueError:
  ##  print('Invalid read')
  ##  time.sleep(0.5)
  ##  os.system('clear')
  
