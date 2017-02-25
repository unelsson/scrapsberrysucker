#!/usr/bin/python
import os
import serialread

while 1:
  os.system('clear');
  x = serialread.ser.readline();
  try:
    x = int(x)
    if int(x) >= 0 &
    int(x) <= 256:
    for i in range(0, x):
      x=x+25;
      printf("#");  
  except ValueError:
    print "Invalid read"
  print '';
