# Scrapsberry Sucker
# Languages: python3, arduino
# http://robotshop.com/letsmakerobots/scrapsberry-sucker

Hoovering robot code etc

Download all files to Raspberry, upload arduino code. Run scrapsberry_core.py with python3.

Files:

index.html - Webinterface for communicating with scrapsberry_core.py. Relays gamepad info to scrapsberry core through websockets. Includes links to run small .py programs with the help of WSGI (a bit outdated now as websocket was implemented).

scrapsberry_core.py - Core Raspberry Pi code, python 3 (run: python3 scrapsberry_core.py)
Includes keyboard control that can be used via ssh. WASD-controls, Gamepad-mode, servo control. Development version of IR map builder and particle filter (that doesn't really work). Serial communication to Arduino. Talks to scrapsberry_core.py through serial com and index.html through websockets.

serialrw.py - Serial communication settings

sketchbook/Scrapsberry.ino - Arduino code (update to arduino: make upload)
Follows instructions from scrapesberry_core.py. Handles DC motors, IR sensor, IR-servo movement. Talks with scrapsberry_core.py.
