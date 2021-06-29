from typing import Dict
from scipy import signal
import numpy as np
from scipy.integrate import odeint
import functions as fn
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.pylab import *
from numpy.linalg import norm

##Definicion de Parametros iniciales para vehiculo diferencial
b = 19.5 #[mm]
r = 1.2  #[mm]
ts = 0.5

t = np.arange(0, 1000, 0.5)
Ty = np.zeros((3,1))
Tk = np.zeros((3,1))

#Condiciones Iniciales Para vehiculo
ykV = np.array([0.1])
xkV = np.array([0.1])
theta_kV = np.array([0.1])


#Condiciones iniciales para Vehiculo
wDV = np.array([0.1])
wIV = np.array([0.1])
tAngV = np.array([0.1])


#FK

xe = np.array([0.1])
P = np.array([0.1])
R = np.array([0.1])

Fy = np.array([0.1])
Fx = np.array([0.1])

#rpm_m1 = (pulsos_m1/ppv)*((millis()/60)/60); #solo un dato
#pm_m2 = (pulsos_m2/ppv)*((millis()/60)/60); #Solo un motor


#generacion de señales para motores
def MotorSignalTrayectoria():
    global t
    #señal de velocidad motor derecho
    wD = signal.lti([9.5], [1.0, 1.0])
    tmD, wDs = signal.step(wD,T=t)

    #Señal de velocidad motor izquierdo
    wI = signal.lti([10], [1.0, 1.0])
    tmI, wIs = signal.step(wI,T=t)
    
    return tmI,wIs,tmD,wDs


#xk = np.zeros((3,3))
#pk = np.zeros((3,3))

#xkt = np.zeros((3,3))
#pkt = np.zeros((3,3))


#generar Trayectoria deseada en base a señales establecidas
def TrajectoryPoints(wI,wD):
    global r,b        
    #Variables necesarias para modelo
    Ix = np.array([0.1])
    Iy = np.array([0.1])
    It = np.array([0.1])

    Dx = np.array([0.1])
    Dy = np.array([0.1])
    Dt = np.array([0.1])
    
    #posicion inicial
    Iy[0] = 0
    Ix[0] = 0

    #orientacion inicial
    It[0] = 90*(np.pi/180)

    #salidas del modelo integradas
    for x in range(wI.__len__()):
        resModel = fn.modelo(wD[x],wI[x],It[x],0.5,r,b)
        Ix = np.append(Ix,[resModel[0]+Ix[x-1]])
        Iy = np.append(Iy,[resModel[1]+Iy[x-1]])
        It = np.append(It,[resModel[2]+It[x-1]])

        Dx = np.append(Dx,[resModel[0]])
        Dy = np.append(Dy,[resModel[1]])
        Dt = np.append(Dt,[resModel[2]])
    return Ix,Iy,It,Dx,Dy,Dt

def Tracking(Dx,Dy):
    global r,b    
        
    #Variables necesarias para modelo
    tDwd = np.array([0.1])
    tDwi = np.array([0.1])

    Ox = np.array([0.1])
    Oy = np.array([0.1])
    Ot = np.array([0.1])

    theta = np.array([0.1])
    
    #posicion inicial
    tDwd[0] = 0
    tDwi[0] = 0
    theta[0] = 90*(np.pi/180)

     #Ejecucion de modelo inverso para seguimiento
    #==============================================================================    
    for x in range(Dx.__len__()):
        #modelo inverso para seguimiento de trayectoria
        #obtenemos velocidades angulares mediante cinemcatica inversa
        modelInv = fn.modeloInv(Dx[x]-Ox[x],Dy[x]-Oy[x],Dt[x]-Ot[x]s,0.5,r,b)

        tDwd = np.append(tDwd,[modelInv[0]])
        tDwi = np.append(tDwi,[modelInv[1]])   

        #ejecutamos posible ruta de ejecucion
        model = fn.modelo(tDwd[x],tDwi[x],Ot[x],0.5,r,b)
        
        Ox = np.append(Ox,model[0])
        Oy = np.append(Oy,model[1])
        Ot = np.append(Ot,model[2])

        #salida de ejecucion
    return tDwd,tDwi

#generar Trayectoria deseada en base a señales establecidas
def Vehiculo(tDwi,tDwd):
    global r,b   

    #Variables necesarias para modelo
    IxV = np.array([0.1])
    IyV = np.array([0.1])
    ItV = np.array([0.1])

    DxV = np.array([0.1])
    DyV = np.array([0.1])
    DtV = np.array([0.1])
    
    #posicion inicial
    IyV[0] = 0
    IxV[0] = 0

    DyV[0] = 0
    DxV[0] = 0

    #orientacion inicial
    ItV[0] = 90*(np.pi/180)


    #salidas del modelo integradas
    for x in range(tDwd.__len__()):

        resModel = fn.modelo(tDwd[x],tDwi[x],ItV[x],0.5,r,b)
        IxV = np.append(IxV,[resModel[0]+IxV[x-1]])
        IyV = np.append(IyV,[resModel[1]+IyV[x-1]])
        ItV = np.append(ItV,[resModel[2]+ItV[x-1]])

        DxV = np.append(DxV,[resModel[0]])
        DyV = np.append(DyV,[resModel[1]])
        DtV = np.append(DtV,[resModel[2]])
    return IxV,IyV,ItV,DxV,DyV,DtV

def init():
    global theta,xk,yk,theta_k,patch,tmI,wIs,tmD,wDs,lineTra,direction
    patch.center = (0, 0)
    ax05.add_patch(patch)
    ax05.add_patch(direction)
    mIzq.set_data([], [])
    mDer.set_data([], [])
    mIzqS.set_data([], [])
    mDerS.set_data([], [])
    Track.set_data([], [])
    
    return patch,mIzq,mDer,Tracyec,direction,mIzqS,mDerS,Track



def animate(index,tI,tD,wI,wD,tDwi,tDwd,IxV,IyV):
    global patch,lineTra,direction
    #ajuste de escala mIza - mDer
    #mIzq.set_data(tmI[0:index],wIs[0:index]*r)
    #mDer.set_data(tmD[0:index],wDs[0:index]*r)

    #Velocidades angulares Trayectoria
    mIzq.set_data(tI[0:index],wI[0:index])
    mDer.set_data(tD[0:index],wD[0:index])

    #velocidades angulares Seguimiento
    mIzqS.set_data(tI[0:index],tDwi[0:index]) 
    mDerS.set_data(tD[0:index],tDwd[0:index])
   

    #trayectoria a seguir
    Track.set_data(IxV[0:index],IyV[0:index])

    #Animacion de seguimiento
    patch.center = (x[index], y[index])
    direction = plt.Arrow(x[index], y[index],(b*2)*math.cos(t[index]),(b*2)*math.sin(t[index]), width = 10)
    ax05.add_patch(direction)
    return patch,mIzq,mDer,Tracyec,direction,mIzqS,mDerS,Track

if __name__ == "__main__":    
    
    fig = plt.figure(num = 0, figsize = (10, 30))#, dpi = 100)
    fig.suptitle("Seguimiento de Trayectoria", fontsize=12)
    ax01 = subplot2grid((3, 2), (0, 0))
    ax02 = subplot2grid((3, 2), (0, 1))
    ax03 = subplot2grid((3, 2), (1, 0))
    ax04 = subplot2grid((3, 2), (1, 1))
    ax05 = subplot2grid((3, 2), (2, 0), colspan=2, rowspan=1)

    ###########Definir titulos################
    ax01.set_title('Motor Izquierdo Trayectoria')
    ax02.set_title('Motor Derecho Trayectoria')
    ax03.set_title('Motor Izquierdo Seguimiento')
    ax04.set_title('Motor Derecho Seguimiento')
    ax05.set_title('Seguimiento')

    # 
    ###########set y-limits################
    ax01.set_ylim(0,15)
    ax02.set_ylim(0,15)
    ax03.set_ylim(0,15)
    ax04.set_ylim(0,15)
    ax05.set_ylim(-400,400)

    ###########set y-limits################
    ax01.set_xlim(0,10)
    ax02.set_xlim(0,10)
    ax03.set_xlim(0,10)
    ax04.set_xlim(0,10)
    ax05.set_xlim(-200,500)

    ##################Grid################
    ax01.grid(True)
    ax02.grid(True)
    ax03.grid(True)
    ax04.grid(True)
    ax05.grid(True)

    #Generar Trayectoria con señales determinadas
    tI,wI,tD,wD = MotorSignalTrayectoria()
    x,y,t,Dx,Dy,Dt =TrajectoryPoints(wI,wD)
    tDwd,tDwi = Tracking(Dx,Dy)
    IxV,IyV,ItV,DxV,DyV,DtV = Vehiculo(tDwd,tDwi)

    #dibujar vehiculo
    patch = plt.Circle((5, -5), 19.5, fc='y')
    #direccion y orientacion
    direction = plt.arrow(0, 0, 0,0, width = 10)

    #inician graficas de motores
    mIzq, = ax01.plot([], [], lw=2)
    mDer, = ax02.plot([], [], lw=2)
    mIzqS, = ax03.plot([], [], lw=2)
    mDerS, = ax04.plot([], [], lw=2)

    #inicia grafica de trayectoria
    Tracyec, = ax05.plot(x, y, lw=1)

    #marca de seguimiento
    Track, = ax05.plot([], [], lw=1)
    #mIzq, = ax01.plot(tI,wI)

    #ejecucion de modelo
    anim = animation.FuncAnimation(fig, animate,init_func=init,fargs=[tI,tD,wI,wD,tDwi,tDwd,IxV,IyV,],frames=1000,interval=10,blit=True)
    
    plt.show()
        
        #aplicacion filtro de kalman
        #ResEst = fn.kalmanF(xk[x],yk[x],theta_k[x],theta_k[x-1],V[x-1],w[x-1],xe[x],P[x],R[x]) #ejecucion de filtro de kalman
        #xe = np.append(xe,[ResEst[1]])
        #P = np.append(P,[ResEst[2]])
        #R = np.append(R,[ResEst[3]])

        #==========================================<=====================


        #Tk = Tk + xk
        #Rx = np.append(Rx,[Ty[0]]) 
        #Ry = np.append(Ry,[Ty[1]])

        
        #resp = ResEst[0]
        #theta = np.append(theta,[Ty[2]])
        #Fx = np.append(Fx,[resModel[0]])
        #Fy = np.append(Fy,[resModel[1]])