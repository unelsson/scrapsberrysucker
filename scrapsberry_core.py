#!/usr/bin/python3
import os
import sys
import tty
import termios
import serialrw
import time
import cv2
import numpy as np
import math
import random
import urllib.request

random.seed()

serreaddata = ['/0']*19 #List for storing latest IR scan data
irdistdata = [0]*19 #Latest IR scan data converted to distances

mapsize = 100		#Map settings, robotx and roboty are map coordinates
#map = np.zeros((mapsize,mapsize)) #OLD MAP, 1 unit of map is 10cm
map = np.full((mapsize,mapsize,3), [100,100,100]);  #Opencv2 img-type map
map2 = np.full((mapsize,mapsize,3), [100,100,100]); #Map with particlefilterdots
robotx = mapsize / 2
roboty = mapsize / 2
visionx = 0
visiony = 0
robotangle = 0.000

particles = 25 #Amount of particles
particlefilter = np.array([[round(robotx), round(roboty), robotangle, 0.5]]*particles)
 
# This code was modified from pyimagesearch.com
# Test code for opening a snapshot to opencv2 from mjpg-streamer
#resp = urllib.request.urlopen('http://127.0.0.1:8080/?action=snapshot" /')
#image = np.asarray(bytearray(resp.read()), dtype="uint8")
#image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#cv2.imwrite('camerass.jpg',image)

ch = 0 #Keyboard input


def read_ch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readarduinoserial():
    for i in range(0, 19):
        serread = serialrw.ser.readline()
        serreaddata[i] = int(serread.decode('ascii').strip('\r\n'))
        if serreaddata[i] < 70: irdistdata[i]=10
        if serreaddata[i] <= 96 & serreaddata[i] > 70: irdistdata[i]=4
        if serreaddata[i] <= 120 & serreaddata[i] > 96: irdistdata[i]=3
        if serreaddata[i] <= 180 & serreaddata[i] > 120: irdistdata[i]=2
        if serreaddata[i] <= 235 & serreaddata[i] > 180: irdistdata[i]=2
        if serreaddata[i] <= 250 & serreaddata[i] > 235: irdistdata[i]=1
        if serreaddata[i] > 250: irdistdata[i]=1
        # Interpreting look() values (Sharp IR mean average)
        # 60-70 (free view, almost)
        #   96 (2 * A4 paper)
        #   120 (1,5 * A4 paper)
        #   180 (1 * A4 paper)
        #   235 (0,5 * A4 paper)
        print('debug1')


def drawmap():
    for i in range(0, 19):
        if int(irdistdata[i]) > 0:
            for k in range(0, irdistdata[i]+1):
                drawpointerx = round(robotx + math.sin(robotangle-1.57+i*0.174)*k)
                drawpointery = round(roboty + math.cos(robotangle-1.57+i*0.174)*k)
                temporaryb = map[drawpointerx, drawpointery,0]
                temporaryg = map[drawpointerx, drawpointery,1]
                temporaryr = map[drawpointerx, drawpointery,2]
                lightenedb = temporaryb + 70
                lightenedg = temporaryg + 70
                lightenedr = temporaryr + 70
                darkenedb = temporaryb - 30
                darkenedg = temporaryg - 30
                darkenedr = temporaryr - 30
                if lightenedb > 255: lightenedb = 255
                if lightenedg > 255: lightenedg = 255
                if lightenedr > 255: lightenedr = 255
                if darkenedb > 255: darkenedb = 255
                if darkenedg > 255: darkenedg = 255
                if darkenedr > 255: darkenedr = 255
                if lightenedb < 0: lightenedb = 0
                if lightenedg < 0: lightenedg = 0  
                if lightenedr < 0: lightenedr = 0
                if darkenedb < 0: darkenedb = 0
                if darkenedg < 0: darkenedg = 0
                if darkenedr < 0: darkenedr = 0
                if drawpointerx > 0 and drawpointerx < mapsize and drawpointery > 0 and drawpointery < mapsize:
                    if k < irdistdata[i]: map[(drawpointerx, drawpointery)] = [darkenedb,darkenedg,darkenedr]
                    if k == irdistdata[i] and irdistdata[i] < 9: map[(drawpointerx, drawpointery)] = [lightenedb,lightenedg,lightenedr]


def moveparticles(move, turn):     #move forward in cm*10, turn right in radian
    for i in range(0, particles):
        particlefilter[i,2] = particlefilter[i,2] + turn
        particlefilter[i,0] = round(particlefilter[i,0] + math.sin(particlefilter[i,2])*move)
        particlefilter[i,1] = round(particlefilter[i,1] + math.cos(particlefilter[i,2])*move)
        particlefilter[i,3] = particlefilter[i,3]


def updateparticles():
    for i in range(0, particles):
        particlefilter[i,2] = particlefilter[i,2] + random.randint(0,99)/1000
        particlefilter[i,0] = round(particlefilter[i,0])
        particlefilter[i,1] = round(particlefilter[i,1])
        particlefilter[i,3] = particlefilter[i,3]

def resampleparticles():
    for i in range(0, particles):
        for j in range(0, 19):
            seewall = 0
            k = 0
            while k < irdistdata[j]+1 and seewall == 0:
                drawpointerx = round(particlefilter[i,0] + math.sin(particlefilter[i,2]-1.57+j*0.174)*k)
                drawpointery = round(particlefilter[i,1] + math.cos(particlefilter[i,2]-1.57+j*0.174)*k)
                if map[drawpointerx, drawpointery, 0] > 122:
                    seewall = 1
                    if math.fabs(k-irdistdata[j] < 3):
                        particlefilter[i,3] = particlefilter[i,3] + map[drawpointerx, drawpointery,0]/255
                k = k + 1
    maxweight = np.amax(particlefilter[:,3])
    for i in range(0, particles):
        particlefilter[i, 3] = particlefilter[i,3] / maxweight
    sortedparticlefilter = np.flipud(particlefilter[np.argsort(particlefilter[:, 3])])
    c = 0
    for i in range(0, particles):
        if sortedparticlefilter[i,3] < 0.2 or i > (particles-5):
            sortedparticlefilter[i,0] = sortedparticlefilter[0+c, 0] + random.randint(0, 4) - 2
            sortedparticlefilter[i,1] = sortedparticlefilter[0+c, 0] + random.randint(0, 4) - 2
            sortedparticlefilter[i,2] = sortedparticlefilter[0+c, 0] + random.randint(0,100) / 500
            sortedparticlefilter[i,3] = 0.5
            c = c + 1
    return np.flipud(sortedparticlefilter[np.argsort(sortedparticlefilter[:, 3])])

while 1:
    print('You pressed',ch)
    print('Press W,A,S or D for movement, G for IR scan')
    print('Serial queue waiting (should be 0)', serialrw.ser.inWaiting())
    print('X:', robotx, 'Y', roboty, 'Angle', robotangle)
    print('Serial read (IR scan)', serreaddata)
    print('Particle filter data', particlefilter)
    ch = read_ch()
    if ch=="w":
        serialrw.ser.write(b'w')
        moveparticles(2, 0)       #20cm, 0 angle turn
        updateparticles()
    if ch=="a":
        serialrw.ser.write(b'a')
        moveparticles(0, -0.52)   #-30 degrees
        updateparticles()
    if ch=="s":
        serialrw.ser.write(b's')
        moveparticles(-1, 0)      #-10cm, 0 angle turn
        updateparticles()
    if ch=="d":
        serialrw.ser.write(b'd')
        moveparticles(0, 0.52)    #+30 degrees
        updateparticles()
    if ch=="q":  
        break
    if ch=="g":
        robotangle = particlefilter[0,2] #Use best values for map
        robotx = particlefilter[0,0]
        roboty = particlefilter[0,1]
        serialrw.ser.write(b'g')
        time.sleep(2.5)
        try:
            readarduinoserial()
        except ValueError:
            print('Read error! :)')
        drawmap()
        map2 = map.copy()
        for i in range(0, particles):
            map2[particlefilter[i,0], particlefilter[i,1]] = [0,0,255*particlefilter[i,3]]
        cv2.imwrite('robomap.png', map2)
        particlefilter = resampleparticles()
  
