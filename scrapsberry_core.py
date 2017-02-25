#!/usr/bin/python
import os
import sys
import serialread
import time

while 1:
  os.system('clear');
  print "START";
  x = serialread.ser.readline();
  try:
    x = int(x)
    if int(x) >= 0 & int(x) <= 500:
      print x;
      for i in range(0, x):
        i=i+25;
        print ('#', sep='');
  except ValueError:
    print "Invalid read"
  print "END";
  time.sleep(0.01);
