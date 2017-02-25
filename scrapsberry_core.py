#!/usr/bin/python
import os
import serialread

while 1:
  os.system('clear');
  x = serialread.ser.readline();
  for i in range(0, x):
    x=x+25;
    printf("#");
  print '';
