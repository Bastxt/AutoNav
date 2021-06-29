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
    V = (vI+vD)/2 #velocidad lineal
    w = (wI-wD)/b #velocidad angular
    theta = w*r #angulo de aplicacion

    return [V,w,theta]


def modeloInv(xk,yk,thetak,Ts,r,b):
    #Cinematica directa
    #|  xK      |       #|  (r*(np.cos(theta_k))/2)       (r*(np.cos(theta_k))/2)   |       #|  wD   |
    #|  yK      |   =   #|  (r*(np.sin(theta_k)/2))       (r*(np.sin(theta_k))/2)   |   *   #|  wI   |
    #|  thetaK  |       #|  (r/b)                         (-r/b)                  |

    #Cinematica inversa
    #|  wD      |       #|  (r*(np.cos(theta_k))/2)       (r*(np.sin(theta_k)/2))       (r/b)   |       #|  xk      |
    #|  wI      |   =   #|  (r*(np.cos(theta_k))/2)       (r*(np.sin(theta_k))/2)       (-r/b)  |   *   #|  yk      |
                                                                                                        #|  thetak  |
    #Obtener pseudoinversa de matriz de transformacion
    B = np.matrix([[((Ts*np.cos(thetak))/r),((Ts*np.sin(thetak))/r),Ts*(b/r)],[((Ts*np.cos(thetak))/r),((Ts*np.sin(thetak))/r),Ts*-(b/r)]])
    U = np.matrix([[xk],[yk],[thetak]])

    #se obtiene un vector compuesto por [posicion x, posicion y, Theta]
    return (B*U) #[wD,wI]


def modelo(wD,wI,theta_k,Ts,r,b):
    #Relacionando solo velocidad angular, velocidad xlineal y algulo de aplicacion
    #A = np.matrix([[np.cos(theta),0],[np.sin(theta),0],[0,1]])
    #B = np.matrix([[v],[w]])

    #Entradas del modelo para integracion numerica
    #|  xK      |   posicion actual x
    #|  yK      |   posicion actual y 
    #|  thetaK  |   angulo de orientacion actual
    
    #Matriz de Transformacion B
    #|  cos(theta_k)     0   |
    #|  sin(theta_k)     0   |
    #|  0                1  |

    #Ganancias del sistema U
    #|  Vk   | 10cm/s
    #|  wK   | 0.5 rad/s


    #Se requiere dejar en termino de velocidades angulares wIzq - wDer
    #Velocidad Lineal
    #v = r*((vDer+vIzq)/2)

    #Velocidad Angular
    #w = r*((vDer-vIzq)/b)

    #agrupando de obtiene
    #|  xK      |       #|  (r*(np.cos(theta_k))/2)       (r*(np.cos(theta_k))/2)   |       #|  wD   |
    #|  yK      |   =   #|  (r*(np.sin(theta_k)/2))       (r*(np.sin(theta_k))/2)   |   *   #|  wI   |
    #|  thetaK  |       #|  (r/b)                         (-r/b)                  |


    #Fk = np.matrix([[xk],[yk],[thetak]])
    
    B = np.matrix([[(r*(Ts*np.cos(theta_k))/2),(r*(Ts*np.cos(theta_k))/2)],[(r*(Ts*np.sin(theta_k)/2)),(r*(Ts*np.sin(theta_k)/2))],[Ts*(r/b),Ts*(-r/b)]])

    U = np.matrix([[wD],[wI]])
    #se obtiene un vector compuesto por [posicion x, posicion y, Theta]
    return (B*U) #[x,y,theta]