import numpy as np

def kalmanF(xi,yi,thetai,theta_kb,V_kb,w_kb):

    H = np.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]) #matriz de ajuste
    zk = H * np.matrix([[xi],[yi],[thetai]])
    Ts = 0.5

    #modelo
    F = np.matrix([[Ts*np.cos(theta_kb)*V_kb,0,0]],[0,Ts*np.sin(theta_kb)*V_kb,0],[0,0,Ts*w_kb])

    xe = F*xe;                  # x[n+1|n] 
    P = F*P*np.linalg.inv(F)    # P[n+1|n]

    K = P*np.linalg.inv(H)/(H*P*np.linalg.inv(H)) # actualización de ganancia
    xe = xe + K*(zk-H*xe);  # x[n|n]
    P = (np.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])-K*H)*P;  # P[n|n]

    ye=H*xe #salida estimada
    #theta=ye(3);
    #errcov = H*P*H'; % actualización error covarianza

    ##################################################### 
    return ye