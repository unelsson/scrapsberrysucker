# Scrapsberry Sucker
# Languages: python3, arduino
# http://robotshop.com/letsmakerobots/scrapsberry-sucker

Hoovering robot code etc

Download all files to Raspberry, upload arduino code. Run scrapsberry_core.py with python3.

Files:

scrapsberry_core.py - Core Raspberry Pi code, python 3 (run: python3 scrapsberry_core.py)
Includes keyboard control that can be used via ssh. Serial communication to Arduino.

serialrw.py - Serial communication settings

sketchbook/Scrapsberry.ino - Arduino code (update to arduino: make upload)
Follows instructions from scrapesberry_core.py. Handles DC motors, IR sensor, IR-servo movement.
