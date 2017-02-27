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
  if ch=="w":
    print("Pressed w")
    serialrw.ser.write(b'w')
  if ch=="a":
    print("Pressed a")
    serialrw.ser.write(b'a')
  if ch=="s":
    print("Pressed s")
    serialrw.ser.write(b's')
  if ch=="d":
    print("Pressed d")
    serialrw.ser.write(b'd')
  if ch=="x":
    print("Pressed x")
    serialrw.ser.write(b'x')
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
  
