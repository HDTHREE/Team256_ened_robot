#!/usr/bin/env python
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

diameter=1 #this value represents the diameter of the wheels in cm
circ=pi*diameter

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

def MoveInches(n): MoveDistance(2.54*n)

def TurnAngle(r):
    global pos
    global gyro
    global tankV

    #calculate the angle to turn in degrees
    angle = r * pi / 180
    
    #reset the gyro sensor
    gyro.reset()
    
    #set the motor speeds to turn in place
    if (r > 0): tankV.on(SpeedPercent(50), SpeedPercent(-50))
    else: tankV.on(SpeedPercent(-50), SpeedPercent(50))
    
    #keep turning until the desired angle is reached
    while abs(gyro.angle) < abs(r): pass
    
    #stop the motors and update the heading
    tankV.off()
    heading = gyro.angle
    pos = pos[0], pos[1], heading

class Testing:
    def LocomotionTest1():
        MoveInches(12)
    def LocomotionTest2():
        MoveInches(36)
    def LocomotionTest3():
        MoveInches(60)
    def LocomotionTest4():
        MoveInches(84) 
    def LocomotionTest5():
        MoveInches(12)
        TurnAngle(pi)
        MoveInches(12)
    def LocomotionTest6():
        MoveInches(12)
        TurnAngle(pi)
        MoveInches(24)      
    def LocomotionTest7():
        MoveInches(12)
        TurnAngle(pi)
        MoveInches(48)
    def LocomotionTest8():
        MoveInches(12)
        TurnAngle(pi)
        MoveInches(96)

if __name__ == "__main__":
    Testing.LocomotionTest1