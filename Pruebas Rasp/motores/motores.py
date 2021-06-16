import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.OUT)
gpio.setup(3,gpio.OUT)

Motor= gpio.PWM(4,100)
Motor2= gpio.PWM(3,100)
e=0;
while True:
    Motor.start(0)
    
    for i in range(0,100,25):
        #Motor.ChangeDutyCycle(i)
        #time.sleep(1)
        if i > 50:
            print('Entre: ',i)
            global e;
            if e == 1:
                print('entre');
                Motor2.start(0)                
                Motor2.ChangeDutyCycle(i)
                time.sleep(1)
            else:    
                Motor.stop()               
                time.sleep(1)
                e=1;
        else: 
            Motor.ChangeDutyCycle(i)
            time.sleep(1)
