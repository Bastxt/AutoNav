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

    #primera prueba velocidades Angulares iguales 
    #tercera prueba velocidades distintas (trayectoria circular a la izq)
    #prueba 4 trayectoria circular a la der
    #prueba 5 trayectoria irregular
    #señal de velocidad motor derecho
    #el sobre pico genera una espiral para luego estabilizarse con velocidades diferentes
    wD = signal.lti([8], [1.0, 1.0])
    tmD, wDs = signal.step(wD,0)

    #Señal de velocidad motor izquierdo
    wI = signal.lti([8], [1.0, 1.0, 1.0])
    tmI, wIs = signal.step(wI,0)
    
    return tmI,wIs,tmD,wDs


#xk = np.zeros((3,3))
#pk = np.zeros((3,3))

#xkt = np.zeros((3,3))
#pkt = np.zeros((3,3))


#generar Trayectoria deseada en base a señales establecidas
def TrajectoryPoints():
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

    tI,wI,tD,wD = MotorSignalTrayectoria()

    #salidas del modelo integradas
    for x in range(tI.__len__()):
        resModel = fn.modelo(wD[x],wI[x],It[x],0.5,r,b)
        Ix = np.append(Ix,[resModel[0]+Ix[x-1]])
        Iy = np.append(Iy,[resModel[1]+Iy[x-1]])
        It = np.append(It,[resModel[2]+It[x-1]])

        Dx = np.append(Dx,[resModel[0]])
        Dy = np.append(Dy,[resModel[1]])
        Dt = np.append(Dt,[resModel[2]])
    return Ix,Iy,It,Dx,Dy,Dt

def Tracking():
    global r,b    
    x,y,t,Dx,Dy,Dt =TrajectoryPoints()
    tI,wI,tD,wD = MotorSignalTrayectoria()
    
    #Variables necesarias para modelo
    tIwd = np.array([0.1])
    tIwi = np.array([0.1])

    tDwd = np.array([0.1])
    tDwi = np.array([0.1])
    
    #posicion inicial
    tIwd[0] = 0
    tIwi[0] = 0

     #Ejecucion de modelo inverso para seguimiento
    #==============================================================================    
    for x in range(tI.__len__()):
        #modelo inverso para seguimiento de trayectoria
        modelInv = fn.modeloInv(Dx[x],Dy[x],Dt[x],0.5,r,b)
        tIwd = np.append(tIwd,[modelInv[0]+tIwd[x-1]])
        tIwi = np.append(tIwi,[modelInv[1]+tIwi[x-1]])

        tDwd = np.append(tDwd,[modelInv[0]])
        tDwi = np.append(tDwi,[modelInv[1]])

    return tIwd,tIwi,tDwd,tDwi


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



def animate(index):
    global patch,lineTra,direction
    x,y,t,Dx,Dy,Dt =TrajectoryPoints()
    tI,wI,tD,wD = MotorSignalTrayectoria()
    tIwd,tIwi,tDwd,tDwi = Tracking()

    #ajuste de escala mIza - mDer
    #mIzq.set_data(tmI[0:index],wIs[0:index]*r)
    #mDer.set_data(tmD[0:index],wDs[0:index]*r)

    #Velocidades angulares Trayectoria
    mIzq.set_data(tI[0:index],wI[0:index])
    mDer.set_data(tD[0:index],wD[0:index])

    #velocidades angulares Seguimiento
    mIzqS.set_data(tI[0:index],tDwi[0:index]) 
    mDerS.set_data(tD[0:index],tDwd[0:index])

    #objetener angulo con velocidades calculadas
    #PreV = fn.pre_proceso(wDV[index-1],wIV[index-1],r,b)        
    #thetaV = np.append(thetaV,[PreV[2]])

    #Gk = np.matrix([[xkV[index-1]],[ykV[index-1]],[thetaV[index-1]]])

    #ModeloPOS = fn.modelo(xkV[index-1],ykV[index-1],thetaV[index-1],wDV[index],wIV[index],theta_kV[index],0.5,r,b)

    #realimentar variables de vehiculos
    #xkV = np.append(xkV,[ModeloPOS[0]])
    #ykV = np.append(ykV,[ModeloPOS[1]])
    #theta_kV = np.append(theta_kV,[ModeloPOS[2]])
    

    #trayectoria a seguir
    #Track.set_data(xkV[0:index],ykV[0:index])

    #Animacion de seguimiento
    #patch.center = (x[index], y[index])
    #direction = plt.Arrow(x[index], y[index],(b*2)*math.cos(t[index]),(b*2)*math.sin(t[index]), width = 10)
    #ax05.add_patch(direction)
    return patch,mIzq,mDer,Tracyec,direction,mIzqS,mDerS,Track

if __name__ == "__main__":    
    
    fig = plt.figure(num = 0, figsize = (8, 30))#, dpi = 100)
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
    ax05.set_ylim(-200,200)

    ###########set y-limits################
    ax01.set_xlim(0,8)
    ax02.set_xlim(0,8)
    ax03.set_xlim(0,8)
    ax04.set_xlim(0,8)
    ax05.set_xlim(-200,200)

    ##################Grid################
    ax01.grid(True)
    ax02.grid(True)
    ax03.grid(True)
    ax04.grid(True)
    ax05.grid(True)

    #Generar Trayectoria con señales determinadas
    tI,wI,tD,wD = MotorSignalTrayectoria()
    x,y,t,Dx,Dy,Dt = TrajectoryPoints()

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
    Tracyec, = ax05.plot(x, y, lw=2)

    #marca de seguimiento
    Track, = ax05.plot([], [], lw=1)
    #mIzq, = ax01.plot(tI,wI)

    #ejecucion de modelo
    anim = animation.FuncAnimation(fig, animate,init_func=init,frames=100,interval=100,blit=True)
    
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