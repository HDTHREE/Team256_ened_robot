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
    print(wheelTheta)

    #reset motor positions
    m1.position = 0
    m2.position = 0
    
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(20),SpeedPercent(20), wheelTheta, brake=True, block=True)
    
    #reset the gyro sensor for the next movement
    gyro.reset()
    sleep(0.5)

def goBackwards():
    global m1
    global m2
    global gyro
    global tankV
    
    #calculate the distance each wheel needs to travel
    
    #reset motor positions
    m1.position = 0
    m2.position = 0
    
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(20),SpeedPercent(20), -43.320, brake=True, block=True)
    
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

def MoveMin():
    global m1
    global m2
    global gyro
    global tankV

    #reset motor positions
    m1.position = 0
    m2.position = 0
    tankV.off(brake=True)
    #set motor speeds
    tankV.on_for_degrees(SpeedPercent(10),SpeedPercent(10), 12, brake=True, block=True)
    
    #reset the gyro sensor for the next movement
    gyro.reset()
    sleep(2)

def ReadBarcode():
    global reader
    global m1
    global m2
    global gyro
    global tankV#you suck, how tf did you forget this shit
    sleep(3)
    color=[0,0,0,0]
    color[0]=reader.color
    MoveMin()#just move dont scan
    MoveMin()
    color[1]=reader.color
    MoveMin()
    color[2]=reader.color
    MoveMin()
    color[3]=1
    MoveMin()

    for i in range(len(color)):    
        if(color[i]==1): {}
        else: color[i]=6

    
    color[3]=1

    binInt=0
    for i in range(len(color)): 
        if(color[i]==1): 
            binInt = binInt + (2**i)

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
        global ReadBarcode
        MoveDistance(10)
        sleep(1.5)
        code=ReadBarcode()
        outputStr=""
        outputStr2="Unidentified box"
        if(code==testCode): outputStr = "CODE MATCHES: "
        else: outputStr= "CODE DOESN'T MATCH: "
        if(code==8): outputStr2="Box type 1"
        if(code==10): outputStr2="Box type 2"
        if(code==12): outputStr2="Box type 3"
        if(code==9): outputStr2="Box type 4"
        lcd=Display()
        lcd.clear()
        lcd.draw.text((50,50), outputStr)
        lcd.draw.text((50,60), outputStr2)
        lcd.draw.text((50,70), str(code))
        print(code)
        lcd.update()
        sleep(5)
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

        TurnAngle(90)
        MoveDistance(17)

        #drop
        Drop()

if __name__ == "__main__":
    Subtasks.Subtask4()