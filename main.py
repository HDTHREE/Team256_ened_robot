#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import GyroSensor
from time import sleep
from math import pi, sin, cos

leftPort=OUTPUT_A
rightPort=OUTPUT_B
gyroPort=INPUT_1
distConst=0

m1 = LargeMotor(leftPort)
m2 = LargeMotor(rightPort)
tankV = MoveTank(leftPort,rightPort)

gyro = GyroSensor(gyroPort)
gyro.calibrate()
pos=0,0,0 #x,y,theta
gyro.reset()

def MoveDistance(n):
    global pos
    global gyro
    global tankV
    global distConst
    global circ
    
    #calculate the distance each wheel needs to travel
    wheelDist = n*circ
    
    #reset motor positions
    m1.position = 0
    m2.position = 0
    
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(50),SpeedPercent(50), wheelDist, brake=True, block=True)
    
    #calculate the distance traveled using the average of the two wheel positions
    posChange = ((m1.position + m2.position) / 2) * circ / 360
    
    #update the position and heading using the gyro sensor
    heading = gyro.angle
    posX = pos[0] + (posChange + distConst) * cos(heading * pi / 180)
    posY = pos[1] + (posChange + distConst) * sin(heading * pi / 180)
    pos = posX, posY
    
    #reset the gyro sensor for the next movement
    gyro.reset()

if __name__ == "__main__":
    MoveDistance(10)