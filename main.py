#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.display import *
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from time import sleep
from math import pi, sin, cos

leftPort=OUTPUT_A
rightPort=OUTPUT_B
mediumPort=OUTPUT_D
gyroPort=INPUT_2

distConst=0
colorPort=INPUT_3
liftVal=150

gyro = GyroSensor(gyroPort)
gyro.calibrate()
gyro.reset()

reader = ColorSensor(colorPort)

m1 = LargeMotor(leftPort)
m2 = LargeMotor(rightPort)
m3 = MediumMotor(OUTPUT_D)
tankV = MoveTank(leftPort,rightPort)
tankV.gyro=gyro

diameter=2.2*2.54 #this value represents the diameter of the wheels in cm
circ = pi*diameter

def MoveDistance(n):
    global m1
    global m2
    global gyro
    global tankV
    
    #calculate the distance each wheel needs to travel
    if(n<60): wheelTheta = (1.625)*(n/(diameter/2))*(180/pi)
    else: wheelTheta = (1.5)*(n/(diameter/2))*(180/pi)
    
    #reset motor positions
    m1.position = 0
    m2.position = 0
    
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(20),SpeedPercent(20), wheelTheta, brake=True, block=True)
    
    #reset the gyro sensor for the next movement
    gyro.reset()
    sleep(0.5)

def TurnAngle(d):
    global m1
    global m2
    global gyro
    global tankV

    gyro.reset()

    tankV.turn_degrees(SpeedPercent(5), -d, brake=True, error_margin=3, sleep_time=0.01)

    gyro.reset()

def ReadBarcode():
    global reader

    color=[]
    color[0]=reader.color
    MoveDistance(0.5)
    color[1]=reader.color
    MoveDistance(0.5)
    color[2]=reader.color
    MoveDistance(0.5)
    color[3]=reader.color
    MoveDistance(0.5)

    for i in range(len(color)):    
        if(color[i]==1): {}
        else: color[i]=6

    binInt=0
    for i in range(len(color)): 
        if(color[i]==1): 
            binInt+=(2**i)

    return binInt
    
def Lift():
    global m3
    global liftVal

    m3.on_for_degrees(SpeedPercent(-20), liftVal, brake=True, block=True)

def Drop():
    global m3
    global liftVal
    
    m3.on_for_degrees(SpeedPercent(40), liftVal, brake=True, block=True)

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
    def Subtask3(testCode):#input as binary interpretation
        MoveDistance(10)
        code=ReadBarcode()
        Display.update()
        if(code==testCode): Display.text_pixels("CODE MATCHES {0}".format(code), clear_screen=True, text_color='black')
        else: Display.text_pixels("CODE DOESN'T MATCH {0}".format(code), clear_screen=True, text_color='black')
    def Subtask4():
        #does three left hand turns and sets the robot to the pickup location
        MoveDistance(6)
        TurnAngle(90)
        MoveDistance(3)
        TurnAngle(90)
        MoveDistance(6)
        TurnAngle(90)
        MoveDistance(3.3)

        #lifts
        Lift()

        MoveDistance(-1.3)
        TurnAngle(90)
        MoveDistance(14)

        #drop
        Drop()

if __name__ == "__main__":
    MoveDistance(96)