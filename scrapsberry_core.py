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
  print("Decoded", x.decode('utf-8'))
  ch = read_ch()
  print(ch)
  if ch=="w":
    print("Pressed w")
    serialrw.ser.write(bytes(0, 'UTF-8'))
  if ch=="a":
    print("Pressed a")
    serialrw.ser.write(bytes(1, 'UTF-8'))
  if ch=="s":
    print("Pressed s")
    serialrw.ser.write(bytes(2, 'UTF-8'))
  if ch=="d":
    print("Pressed d")
    serialrw.ser.write(bytes(3, 'UTF-8'))
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
  
