# _*_ coding:utf-8 _*_
# dependencias principales

from sys import path
from os import system, name 
path.append(".")
import RPi.GPIO as gpio
from motorManage import *
import time 

init_pro = time.time()



def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

if __name__ == "__main__":
    motor1 = motor(21, 20, 2, 3,time.time()-init_pro)
    #motor2 = motor(9, 10, 17, 27,time.time())
    motor1.get_freqA.start(0)
    #motor2.get_freqA.start(0)
    while True:
        motor1.DC(50, 0, 0)       
        #motor2.DC(50, 0, 0)
        #pulsos = motor1.get
        print("motor1: "+ str(motor1.calRpm()))
    pass
