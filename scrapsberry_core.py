#!/usr/bin/python
from __future__ import print_function
import os
import sys
import serialread
import time

while 1:
  x = serialread.ser.readline();
  print(x); 
  try:
    x = int(x)
    if int(x) >= 0 & int(x) <= 500:
      print(x);
      for i in range(0, x, 25):
        print ('#', end='');
  except ValueError:
    print('Invalid read');
    os.system('clear');
  time.sleep(0.01);
