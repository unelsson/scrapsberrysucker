#!/usr/bin/python
import os
import sys
import serialread
import time

while 1:
  os.system('clear');
  x = serialread.ser.readline();
  try:
    x = int(x)
    if int(x) >= 0 & int(x) <= 256:
      for i in range(0, x):
        x=x+25;
        print 'x',;
  except ValueError:
    print "Invalid read"
  print '';
  time.sleep(0.01);
