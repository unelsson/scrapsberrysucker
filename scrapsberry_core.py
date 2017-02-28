#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np
import pygame
from pygame.locals import *

def read_ch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def read_pgch():
  for event in pygame.event.get():
    if (event.type == KEYDOWN):
      print(event)
      if (event.key == K_q):
        return 'q'
      if (event.key == K_g):
        return 'g'
    else:
      return '-1'

def main():
  os.environ["SDL_VIDEODRIVER"] = "dummy"
  pygame.init()
  pygame.display.set_mode((1,1))
  while 1:
    #ch = read_ch()
    ch = read_pgch()
    print(ch)
    serialrw.ser.write(bytes(ch, 'ascii')); # Send pressed character to Arduino as bytes
    if ch=="q":  
      break
    print(serialrw.ser.inWaiting())
    if serialrw.ser.inWaiting() > 18: 
      serialrw.ser.flush()
    if serialrw.ser.inWaiting() == 18:
      try:
        for i in range(0, 19): #Receive values
          serread = serialrw.ser.readline()
          print(serread.decode('ascii'))
          j = int(serread)
          #if j >= 0 & j <= 500:
          #for i in range(0, j, 25):
          #  print('#', end='')
          #print('')
      except ValueError:
        print('Invalid read')
        
main()
