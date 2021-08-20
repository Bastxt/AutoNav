import RPi.GPIO as gpio
import time
import picamera

import socket
import sys


t_ime=time.time()

gpio.setmode(gpio.BCM)

#Pirmer motor
gpio.setup(2,gpio.OUT)  #PWM1D
gpio.setup(3,gpio.OUT)  #PWM!

#Segundo motor
gpio.setup(17,gpio.OUT)  #PWM1Z
gpio.setup(27,gpio.OUT)  #PWM!

#Primer Encoder
gpio.setup(20,gpio.IN) 
gpio.setup(21,gpio.IN)

#Segundo Encoder
gpio.setup(19,gpio.IN) 
gpio.setup(26,gpio.IN)

Motor1D= gpio.PWM(2,100)
Motor1Z= gpio.PWM(3,100)

Motor2D= gpio.PWM(17,100)
Motor2Z= gpio.PWM(27,100)
e=0
t=0
#Motor Derecho
CountA=0
CountB=0
pul_ant=0
Pulsos=0
Vel=0
in1_time=0
in2_time=0
rpm_mot=0
rpm_enc=0
#Motor Izquierdo
CountAM2=0
CountBM2=0
pul_antM2=0
PulsosM2=0
in1_timeM2=0
in2_timeM2=0
rpm_motM2=0
rpm_encM2=0
Vel=0
Dir=0


finVideo=1

#Derecha Primer motor
def M1rigth(PINA1,PINB1):
    global Pulsos
    Motor1D.ChangeDutyCycle(PINA1)
    Motor1Z.ChangeDutyCycle(PINB1)

#Izquierda Primer Motor
def M1left(PINA1,PINB1):
    Motor1Z.ChangeDutyCycle(PINA1)
    Motor1D.ChangeDutyCycle(PINB1)

#Derecha Segundo motor
def M2rigth(PINA1,PINB1):
    global Pulsos
    Motor2D.ChangeDutyCycle(PINA1)
    Motor2Z.ChangeDutyCycle(PINB1)

#Izquierda Segundo motor
def M2left(PINA1,PINB1):
    Motor2Z.ChangeDutyCycle(PINA1)
    Motor2D.ChangeDutyCycle(PINB1)

def stop():
    Motor1D.stop()
    Motor2D.stop()

def puto(PINA1,PINB1):
    gpio.output(PINA1,1)
    gpio.output(PINB1,1)

def cheDir():
    global Dir
    if gpio.input(20) == 1:
        Dir=-1
    else:
        Dir=1

#Contador Primer Motor.   
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

#Contador Primer Motor.
def CoB(channel):
    global Dir
    global CountB
    global s_ti
    global in2_time
    in2_time=(s_ti)

#Contador Primer Motor.
def CoAIQZ(channel):
    global Dir
    global CountAM2
    global s_ti
    global in1_timeM2
    global PulsosM2
    global pul_antM2
    #cheDir()
    in1_timeM2=(s_ti)
    pul_antM2=(PulsosM2)
    #CountA+=Dir
    CountAM2+=1

#Contador Primer Motor.
def CoBIZQ(channel):
    global Dir
    global CountBM2
    global s_ti
    global in2_timeM2
    in2_timeM2=(s_ti)    
    #CountBM2 += Dir

def cProporcional(salida,error):
    errorRe=salida-error
gpio.add_event_detect(21,gpio.RISING, callback=CoA)
gpio.add_event_detect(20,gpio.RISING, callback=CoB)
gpio.add_event_detect(26,gpio.RISING, callback=CoAIQZ)

#def on_off (Entrada):


    
while True:
    s_ti=time.time()-t_ime 
    Motor1D.start(0)
    Motor1Z.start(0)
    Motor2D.start(0)
    Motor2Z.start(0)
    #Primer Motor
    Pulsos=CountA+CountB
    d_pul=Pulsos-pul_ant
    ti_pul=(s_ti)-(in1_time)
    pul_seg=(d_pul+0.000001)/((ti_pul)+0.000001)
    pul_min=pul_seg*60    
    rpm_enc= pul_min/6     #revoluciones en el encoder p/segundos
    rpm_mot=rpm_enc*0.02
    #--------------------------------------------------------------------
    #Segundo Motor
    PulsosM2=CountAM2+CountBM2
    d_pulM2=PulsosM2-pul_antM2
    ti_pulM2=(s_ti)-(in1_timeM2)
    pul_segM2=(d_pulM2+0.000001)/((ti_pulM2)+0.000001)
    pul_minM2=pul_segM2*60    
    rpm_encM2= pul_minM2/6     #revoluciones en el encoder p/segundos
    rpm_motM2=rpm_encM2*0.02

    M2rigth(21,0)
    M1rigth(20,0)

    """
    if finVideo== 1:
        #M2rigth(13,0)
        #M1rigth(14,0)
        M2rigth(21,0)
        M1rigth(20,0)
        picam=picamera.PiCamera()        
        picam.start_preview()
        picam.start_recording('video3.h264')
        print('Empece la grabacion')
        picam.wait_recording(5)  
        #M2rigth(10,0)
        #stop()
        M2rigth(15,0)

        picam.wait_recording(1)
        print('Segunda Pausa')
        #M2rigth(13,0)
        #stop()
        M2rigth(22,0)
        print('Cambie Velocidad del motor otra vez')
        picam.wait_recording(8)
        picam.stop_recording()
        picam.stop_preview()
        picam.close()
        stop()
        finVideo=0
    """
   
               
    e=e+1
    #print('RPM motor Der:',rpm_mot,'RPM enconder:',rpm_enc,'e:',e,'t:',t)
    #print('RPM motor Izq:',rpm_motM2,'RPM enconder:',rpm_encM2,'e:',e,'t:',t)
    
    # Configuracion de Socket Cliente
    #  TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Direccion y puerto en escucha
    server_address = ('192.168.39.142', 10000)

    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    
    try:
        # Send data
        message = '304,200'
        print('sending: ',message)
        message = message.encode()
        
        sock.send(message)

        # Look for the response
        amount_received = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        amount_expected = len(message)
    except ValueError:
        print('closing socket')
        sock.close()


    print(' ')
    time.sleep(0.5)
    

    