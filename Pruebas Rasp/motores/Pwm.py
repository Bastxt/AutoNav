import RPi.GPIO as gpio
import time
t_ime=time.time()
in1_time=0
in2_time=0
rpm_mot=0
rpm_enc=0
gpio.setmode(gpio.BCM)

gpio.setup(2,gpio.OUT)  #PWM1D
gpio.setup(3,gpio.OUT)  #PWM!

gpio.setup(20,gpio.IN) #ENCODERB
gpio.setup(21,gpio.IN)

Motor1D= gpio.PWM(2,100)
Motor1Z= gpio.PWM(3,100)

e=0
t=0
CountA=0
CountB=0
pul_ant=0
Pulsos=0
Vel=0
Dir=0
def rigth(PINA1,PINB1):
    global Pulsos
    Motor1D.ChangeDutyCycle(PINA1)
    Motor1Z.ChangeDutyCycle(PINB1)

def left(PINA1,PINB1):
    Motor1D.ChangeDutyCycle(PINA1)
    Motor1Z.ChangeDutyCycle(PINB1)

def stop():
    Motor1D.stop()
    Motor1Z.stop()

def puto(PINA1,PINB1):
    gpio.output(PINA1,1)
    gpio.output(PINB1,1)

def cheDir():
    global Dir
    if gpio.input(20) == 1:
        Dir=-1
    else:
        Dir=1
   
def CoA(channel):
    global Dir
    global CountA
    global s_ti
    global in1_time
    global Pulsos
    global pul_ant
    #cheDir()
    in1_time=(s_ti)
    pul_ant=(Pulsos)
    #CountA+=Dir
    CountA+=1
    '''print('--------------Inicio DENTRO DE LA INTERRUPCION',time.time()-t_ime,'---------------')
    print('S_ti:',s_ti,'int1_ti:',in1_time,'ti_pul:',ti_pul,'Vel:',pul_seg,'CoA:',CountA,'CoB',CountB)
    print('Pulsos:',Pulsos,'pul_ant:',pul_ant,'d_pul:',d_pul)
    print('RPM motor:',rpm_mot,'RPM enconder:',rpm_enc,'e:',e,'t:',t)
    print('--------------Fin DENTRO DE LA INTERRUPCION------------------')'''

def CoB(channel):
    global Dir
    global CountB
    global s_ti
    global in2_time
    in2_time=(s_ti)
    #CountB += Dir

def cProporcional(salida,error):
    errorRe=salida-error
gpio.add_event_detect(21,gpio.RISING, callback=CoA)
gpio.add_event_detect(20,gpio.RISING, callback=CoB)

#def on_off (Entrada):
    
while True:
    s_ti=time.time()-t_ime
    global CountA
    global CountB
    global in1_time
    global pul_ant    
    Motor1D.start(0)
    #Motor1Z.start(0)
    Pulsos=CountA+CountB
    d_pul=Pulsos-pul_ant
    ti_pul=(s_ti)-(in1_time)
    pul_seg=(d_pul+0.000001)/((ti_pul)+0.000001)
    pul_min=pul_seg*60    
    rpm_enc= pul_min/6     #revoluciones en el encoder p/segundos
    rpm_mot=rpm_enc*0.02
    print('--------------Inicio-------------------------------------------')
    print('S_ti:',s_ti,'int1_ti:',in1_time,'ti_pul:',ti_pul,'Vel:',pul_seg)
    print('Pulsos:',Pulsos,'pul_ant:',pul_ant,'d_pul:',d_pul,'CoA:',CountA,'CoB',CountB)
    print('RPM motor:',rpm_mot,'RPM enconder:',rpm_enc,'e:',e,'t:',t)
    print('--------------Fin-------------------------------------------')
    if e > 60:           
        rigth(50,0)
        #print('sube RPM: ',rpm_mot,' RPM encoder: ',rpm_enc)
        #print('Timpo de ejecucion: ',s_ti,'Pulsos: ',Pulsos,'RPM MOTOR:',rpm_mot,'e:',e,'t:',t)
        t=t+1
        if t>30:
            rigth(10,0)
        #time.sleep(0.5) 
    else:
        rigth(3,0)
               
    e=e+1
    time.sleep(0.5)

    