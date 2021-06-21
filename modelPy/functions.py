import numpy as np

'''
def kalmanF(xi,yi,thetai,theta_kb,V_kb,w_kb,xe,P,R):

    H = np.matrix([[1.0,0.1,0.1],[0.1,1.0,0.1],[0.1,0.1,1.0]]) #matriz de ajuste
    zk = H * np.matrix([[xi],[yi],[thetai]])
    Ts = 0.5

    #modelo
    F = np.matrix([[Ts*np.cos(theta_kb)*V_kb,0.1,0.1],[0.1,Ts*np.sin(theta_kb)*V_kb,0.1],[0.1,0.1,Ts*w_kb]])
    
    xe = F*xe;                  # x[n+1|n] 
    P = F*P*np.linalg.pinv(F)    # P[n+1|n]

    K = P*np.linalg.pinv(H)/(H*P*np.linalg.pinv(H)) # actualización de ganancia
    xe = xe + K*(zk-H*xe);  # x[n|n]
    P = (np.matrix([[1.0,0.1,0.1],[0.1,1.0,0.1],[0.1,0.1,1.0]])-K*H)*P;  # P[n|n]

    ye=H*xe #salida estimada
    #theta=ye(3);
    #errcov = H*P*H'; % actualización error covarianza

    ##################################################### 
    return [ye,xe,P,R]
'''

#Esta funcion establece las condiciones iniciales para un vehiculo de tipo diferencial
#parameters:
#   WI  - Velocidad angular Izq obtenida de encoder [Rad/s]
#   WD  - Velocidad angular Der obtenida de encoder [Rad/s]
#   r   - promedio del redio de las llantas del vehiculo [cm]
#   b   - dianetro del vehiculo [cm]

def pre_proceso(wD,wI,r,b):
    vI = wI*r #velocidad motor izq
    vD = wD*r #velocidad motor Der
    V = (vD+vI)/2 #velocidad lineal
    w = (wI-wD)/b #velocidad angular
    theta = w*r #angulo de aplicacion

    return [V,w,theta]



def modelo(xk,yk,thetak,V_k,w_k,theta_k,Ts):
    #v = (vD + vI)/2 #velocidad lineal
    #w = (vD - vI)/l #velocidad angular

    # x = (cos(theta))*(c*(wI+wD)/2)
    # y = (sin(theta))*(c*(wI+wD)/2)
    # theta = (c*(wI-wD)/l)
    #el modelo relaciona velocidad angular velocidad xlineal y algulo de aplicacion
    #A = np.matrix([[np.cos(theta),0],[np.sin(theta),0],[0,1]])
    #B = np.matrix([[v],[w]])

    #mismo modelo añadiendo longitud entre ruedas y radio de la rueda
    ##################################################
    #|1.0    0.1     0.1|
    #|1.0    1.0     0.1|
    #|1.0    0.1     1.0|
    ##################################################
    F = np.matrix([[1.0,0.1,0.1],[0.1,1.0,0.1],[0.1,0.1,1.0]]) #matriz identidad

    ###############Entradas del modelo################
    #|  xK      |
    #|  yK      |
    #|  thetaK  |
    ##################################################
    Fk = np.matrix([[xk],[yk],[thetak]])


    ###############Matriz de Transformacion###########
    #|  Ts*cos(theta_k)     0   |
    #|  Ts*sin(theta_k)     0   |
    #|  0                   Ts  |
    ##################################################
    B = np.matrix([[Ts*np.cos(theta_k),0],[Ts*np.sin(theta_k),0],[0,Ts]])

    ###############Ganancias del sistema##############
    #|  Vk   |
    #|  wK   |
    ##################################################
    U = np.matrix([[V_k],[w_k]])
    #se obtiene un vector compuesto por [posicion x, posicion y, Theta]
    return (Fk)+(B*U) #[x,y,theta]