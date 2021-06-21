from scipy import signal
import numpy as np
import functions as fn
import matplotlib.pyplot as plt
from matplotlib import animation

##Definicion de Parametros iniciales para vehiculo diferencial
b = 19.5 #cm
r = 1.25 # [cm]

Ty = np.zeros((3,1))
Tk = np.zeros((3,1))
yk = np.array([0.1])
xk = np.array([0.1])
theta_k = np.array([0.1])

V = np.array([0.1])
w = np.array([0.1])
theta = np.array([0.1])

xe = np.array([0.1])
P = np.array([0.1])
R = np.array([0.1])

Fy = np.array([0.1])
Fx = np.array([0.1])

#rpm_m1 = (pulsos_m1/ppv)*((millis()/60)/60); #solo un dato
#pm_m2 = (pulsos_m2/ppv)*((millis()/60)/60); #Solo un motor

#señal de velocidad motor derecho
wD = signal.lti([30.0], [1.0, 1.0])
tmD, wDs = signal.step(wD)


#Señal de velocidad motor izquierdo
wI = signal.lti([30.0], [1.0, 1.0, 1.0])
tmI, wIs = signal.step(wI)


#xk = np.zeros((3,3))
#pk = np.zeros((3,3))

#xkt = np.zeros((3,3))
#pkt = np.zeros((3,3))


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-50, 500), ylim=(-50, 500))
patch = plt.Circle((5, -5), 19.5, fc='y')

def TrajectoryPoints():
    global V,w,theta,xk,yk,theta_k,patch,tmI
    for x in range(tmI.__len__()):
        Pre = fn.pre_proceso(wDs[x],wIs[x],r,b)        
        V = np.append(V,[Pre[0]])
        w = np.append(w,[Pre[1]])
        theta = np.append(theta,[Pre[2]])

        resModel = fn.modelo(xk[x-1],yk[x-1],theta[x-1],V[x-1],w[x-1],theta_k[x-1],0.5)
        
        xk = np.append(xk,[resModel[0]])
        yk = np.append(yk,[resModel[1]])
        theta_k = np.append(theta_k,[resModel[2]])
    return xk,yk,theta_k


def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    return patch,

def animate(index):
    global V,w,theta,xk,yk,theta_k,patch,tmI

    Pre = fn.pre_proceso(wDs[index],wIs[index],r,b)        
    V = np.append(V,[Pre[0]])
    w = np.append(w,[Pre[1]])
    theta = np.append(theta,[Pre[2]])

    resModel = fn.modelo(xk[index-1],yk[index-1],theta[index-1],V[index-1],w[index-1],theta_k[index-1],0.5)
    
    xk = np.append(xk,[resModel[0]])
    yk = np.append(yk,[resModel[1]])
    theta_k = np.append(theta_k,[resModel[2]])
    patch.center = (resModel[0], resModel[1])
    return patch,

if __name__ == "__main__":

    #Generar Trayectoria
    x,y,t = TrajectoryPoints()
    #ejecucion de modelo
    anim = animation.FuncAnimation(fig, animate,init_func=init,frames=50,interval=100,blit=True)
    plt.plot(x,y)
    plt.grid()
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