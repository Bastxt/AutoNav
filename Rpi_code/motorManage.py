# _*_ coding:utf-8 _*_
import RPi.GPIO as gpio
import time

class motor():

    __pulsos = 0
    __initTime = 0
    __CountA = 0
    __pulAnt = 0
    __time = 0
    __inTime = 0
   

    def __init__(self, pinA, pinB, outA, outB, iniT):
        global Pulsos
        gpio.setmode(gpio.BCM)
        init_pro = time.time()
        self.__initTime = iniT

        # Configuración de motor
        # configuracion salidas

        gpio.setup(outA, gpio.OUT)  # PWM
        gpio.setup(outB, gpio.OUT)  # PWM!

        # configuración entradas
    
        gpio.setup(pinA, gpio.IN)
        gpio.setup(pinB, gpio.IN)   

        self.__freqA = gpio.PWM(outA, 100)
        self.__freqB = gpio.PWM(outB, 100)

        
        gpio.add_event_detect(pinA, gpio.RISING, callback=self.CoA)
        

    # getters and setters pines de salida (PWM)
    # initTime
    @property
    def get_initTime(self):
        return self.__initTime

    @get_initTime.setter
    def set_initTime(self, initTime):
        self.__initTime = initTime

    # getters and setters duty cycle
    # dcA
    @property
    def get_dcA(self):
        return self._dcA

    @get_dcA.setter
    def set_dcA(self, dcA):
        self._dcA = dcA

    # dcB
    @property
    def get_dcB(self):
        return self._dcB

    @get_dcB.setter
    def set_dcB(self, dcB):
        self._dcB = dcB

    # getters and setters Pulsos
    # _pulsos
    @property
    def get_pulsos(self):
        return self.__pulsos

    @get_pulsos.setter
    def set_pulsos(self, pul):
        self.__pulsos = pul

    # getters and setters FREQ
    # _FREQA
    @property
    def get_freqA(self):
        return self.__freqA

    @get_freqA.setter
    def set_freqA(self,f):
        self.__freqA = f
    
    # _FREQB
    @property
    def get_freqB(self):
        return self.__freqB

    @get_freqB.setter
    def set_freqB(self,f):
        self.__freqB = f

    # Control de velocidad
    def DC(self, dcu, dcd, velObj):
        self.__freqA.ChangeDutyCycle(dcu)
        self.__freqB.ChangeDutyCycle(dcd)


    # getters and setters inTime
    # inTime
    @property
    def get_inTime(self):
        return self._inTime

    @get_inTime.setter
    def set_inTime(self,t):
        self._inTime = t

    # getters and setters inTime
    # __pulAnt
    @property
    def get_pulAnt(self):
        return self.__pulAnt

    @get_pulAnt.setter
    def set_pulAnt(self,p):
        self.__pulAnt = p

    # getters and setters inTime
    # __CountA
    @property
    def get_CountA(self):
        return self._CountA

    @get_CountA.setter
    def set_CountA(self,c):
        self._CountA = c

    # reloj de pulsos
    def CoA(self):
        self.__inTime = (time.time())
        self.__pulsos = self.__CountA
        self.__pulAnt = self.__pulsos
    def CoA(self,):
        self.__inTime = (time.time())
        self.__pulsos = self.__CountA
        self.__pulAnt = self.__pulsos
    def CoA(self,iniT):
     
        self.__inTime = self.__initTime
        #print(self.__inTime)
        #self.__pulsos = self.__CountA
        #self.__pulAnt = self.__pulsos
        self.__pulAnt =  self.__CountA
        self.__CountA += 1
        print(self.__CountA)
        # promedio de pulsos 6000



    def calRpm(self):
        Pulsos=self.__CountA
        #d_pul = (self.get_pulsos)-(self.__pulAnt)
        #tieIni=time.time()-init_pro
        d_pul = ( self.__CountA)-(self.__pulAnt)
        print('di:',d_pul,' pulsos:',self.__CountA,' Pul_ant:',self.__pulAnt)
        print('t_i:',self.__initTime,' t_f:',self.__inTime)
        #ti_pul = ((self.__initTime) - (self.__inTime))
        ti_pul = ((self.__initTime) - (self.__inTime))
        pul_seg = (d_pul+0.000001)/((ti_pul)+0.000001)
        pul_min = pul_seg*60
        rpm_enc = pul_min/6
        rpm_mot=rpm_enc*0.02  # revoluciones en el encoder p/segundos
        #print('RPMS:___'+str(rpm_enc))
        return rpm_mot

    # ex: motor1 = mM.motor(20,21,2,3)
    #se debe correguir la formula, posiblemente son los tiempo, no olvidar!!!!!!! 