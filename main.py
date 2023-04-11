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

gyro = GyroSensor(gyroPort)
gyro.calibrate()
pos=0,0,0 #x,y,theta(degrees)
gyro.reset()

m1 = LargeMotor(leftPort)
m2 = LargeMotor(rightPort)
tankV = MoveTank(leftPort,rightPort)
tankV.gyro=gyro

diameter=2.2*2.54 #this value represents the diameter of the wheels in cm
circ = pi*diameter
def MoveDistance(m):
    n=m/2 
    global pos
    global gyro
    global tankV
    
    #calculate the distance each wheel needs to travel
    wheelTheta = (n/(diameter/2))*(180/pi)
    
    #reset motor positions
    m1.position = 0
    m2.position = 0
    
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(-20),SpeedPercent(-20), wheelTheta, brake=True, block=True)
    
    #calculate the distance traveled using the average of the two wheel positions
    posChange = ((m1.position + m2.position) / 2) * circ
    print(posChange) 
    #should return value close to m

    #update the position and heading using the gyro sensor
    heading = gyro.angle
    posX = pos[0] + (posChange) * cos(heading * (pi / 180))
    posY = pos[1] + (posChange) * sin(heading * (pi / 180))
    pos = posX, posY, (heading%360)
    
    #reset the gyro sensor for the next movement
    gyro.reset()

def TurnAngle(d):
    global pos
    global gyro
    global tankV

    gyro.reset

    tankV.turn_degrees(SpeedPercent(10), d, brake=True, error_margin=1, sleep_time=0.01)

    pos[2] = (pos[2] + d)%360

    gyro.reset

class Subtasks:
    def Subtask1(x):
        MoveDistance(24)
        TurnAngle(-90)
        MoveDistance(x)
        sleep(5)
        MoveDistance(96-x)
        TurnAngle(-90)
        MoveDistance(24)
    def Subtask2():
        TurnAngle(180)
        MoveDistance(6)
        TurnAngle(90)
        MoveDistance(96)
        TurnAngle(90)
        MoveDistance(6)
    
if __name__ == "__main__":
    TurnAngle(-90)