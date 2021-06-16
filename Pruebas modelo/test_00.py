from scipy import signal
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
import numpy as np
import functions as fn

if __name__ == "__main__":
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
    wD = signal.lti([10.0], [1.0, 1.0])
    tmD, wDs = signal.step(wD)
    swD = figure(title="Señal Motor Der.",plot_width=400, plot_height=400)
    swD.circle(tmD,wDs, size=1.5, color="crimson", alpha=0.5)
    swD.xaxis.axis_label = 'Tiempo [s]'
    swD.yaxis.axis_label = 'Velocidad Angular [/s]'

    #Señal de velocidad motor izquierdo
    wI = signal.lti([10.0], [1.0, 1.0, 1.0])
    tmI, wIs = signal.step(wI)
    swI = figure(title="Señal Motor Izq.",plot_width=400, plot_height=400)
    swI.circle(tmI,wIs, size=1.5, color="brown", alpha=0.5)
    swI.xaxis.axis_label = 'Tiempo [s]'
    swI.yaxis.axis_label = 'Velocidad Angular [/s]'

    #xk = np.zeros((3,3))
    #pk = np.zeros((3,3))

    #xkt = np.zeros((3,3))
    #pkt = np.zeros((3,3))

    #ejecucion de modelo
    for x in range(tmI.__len__()):
        Pre = fn.pre_proceso(wDs[x],wIs[x],r,b)
        
        
        V = np.append(V,[Pre[0]])
        w = np.append(w,[Pre[1]])
        theta = np.append(theta,[Pre[2]])

        resModel = fn.modelo(xk[x-1],yk[x-1],theta[x-1],V[x-1],w[x-1],theta_k[x-1],0.5)
        
        xk = np.append(xk,[resModel[0]])
        yk = np.append(yk,[resModel[1]])
        theta_k = np.append(theta_k,[resModel[2]])

        ResEst = fn.kalmanF(xk[x],yk[x],theta_k[x],theta_k[x-1],V[x-1],w[x-1],xe[x],P[x],R[x]) #ejecucion de filtro de kalman
        xe = np.append(xe,[ResEst[1]])
        P = np.append(P,[ResEst[2]])
        R = np.append(R,[ResEst[3]])

        #==========================================<=====================


        #Tk = Tk + xk
        #Rx = np.append(Rx,[Ty[0]]) 
        #Ry = np.append(Ry,[Ty[1]])

        
        resp = ResEst[0]
        #theta = np.append(theta,[Ty[2]])
        Fx = np.append(Fx,[resp[1]])
        Fy = np.append(Fy,[resp[0]])

    #resultados
    resp = figure(title="Posicion",plot_width=400, plot_height=400)
    resp.circle(xk,yk, size=1.5, color="navy", alpha=0.5)
    resp.circle(tmI,theta, size=1.5, color="brown", alpha=0.5)
    resp.circle(Fx,Fy, size=1.5, color="crimson", alpha=0.5)
    resp.xaxis.axis_label = 'Pos X'
    resp.yaxis.axis_label = 'Pos Y'


    show(row(swI,swD,resp))