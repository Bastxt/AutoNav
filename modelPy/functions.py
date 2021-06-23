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

def pre_proceso(wI,wD,r,b):
    vI = wI*r #velocidad motor izq
    vD = wD*r #velocidad motor Der
    V = (vD+vI)/2 #velocidad lineal
    
    w = (wD-wI)/b #velocidad angular
    theta = w*r #angulo de aplicacion

    return [V,w,theta]


def modeloInv(xk,yk,thetak,theta_k,Ts,r,b):

    #Obtener pseudoinversa de matriz de transformacion
    B = np.matrix([[(r*(np.cos(theta_k))/2),(r*(np.sin(theta_k)/2)),(r/b)],[(r*(np.cos(theta_k))/2),(r*(np.sin(theta_k)/2)),-(r/b)]])
    U = np.matrix([[xk],[yk],[thetak]])

    #se obtiene un vector compuesto por [posicion x, posicion y, Theta]
    return (B*U) #[wD,wI]


def modelo(xk,yk,tk,wD,wI,theta_k,Ts,r,b):
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
    #|  Vk   |
    #|  wK   |

    #Se requiere dejar en termino de velocidades angulares wIzq - wDer
    #Velocidad Lineal
    #v = r*((vDer+vIzq)/2)

    #Velocidad Angular
    #w = r*((vDer-vIzq)/b)

    #agrupando de obtiene
    #|  xK      |       #|  (r*(np.cos(theta_k))/2)       (r*(np.cos(theta_k))/2)   |       #|  wD   |
    #|  yK      |   =   #|  (r*(np.sin(theta_k)/2))       (r*(np.sin(theta_k))/2)   |   *   #|  wI   |
    #|  thetaK  |       #|  (r/b)                         (-r/b)                  |

        #agrupando de obtiene
    #|  xK      |       #|  (r*(np.cos(theta_k))/2)       (r*(np.cos(theta_k))/2)   |       #|  wD   |
    #|  yK      |   =   #|  (r*(np.sin(theta_k)/2))       (r*(np.sin(theta_k))/2)   |   *   #|  wI   |
    #|  thetaK  |       #|  (r/b)                         (-r/b)                  |


    #Valores anteriores para integracion numerica
    Fk = np.matrix([[xk],[yk],[tk]])
    
    #x = x(k-1)+Dx 
    #y = y(k-1)+Dy
    #t = t(k-1)+Dt
    
    #B = np.matrix([[Ts*np.cos(theta_k),0],[Ts*np.sin(theta_k),0],[0,Ts]])
    B = np.matrix([[(r*(np.cos(theta_k))/2),(r*(np.cos(theta_k))/2)],[(r*(np.sin(theta_k)/2)),(r*(np.sin(theta_k)/2))],[(r/b),(-r/b)]])

    U = np.matrix([[wD],[wI]]) #valores medidos por sensores
    #se obtiene un vector compuesto por [posicion x, posicion y,s Theta]
    return Fk+(B*U) #[x,y,theta]