import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.pylab import *
import time

trackpoint = np.array([0.1])
nFrame = np.array([0.1])
#media
m = np.array([0.1])

#inicializar
trackpoint[0] = 0
nFrame[0] = 0
m[0] = 0


c =0

fig = plt.figure(num = 0, figsize = (5, 5))#, dpi = 100)
plt.ion()
plt.xlim(0, 600)
plt.grid(True)
plt.show()

for i in range(200):
    trackpoint = np.append(trackpoint,[randint(200,380)])
    nFrame = np.append(nFrame,[c])
    m = np.append(m,[sum(trackpoint)/len(trackpoint)])
    c+=1
    #print('Tamaño: ',len(trackpoint),' |Suma: ',sum(trackpoint),' |Media: ',m)
    plt.plot(trackpoint,nFrame,'bo', lw=2)
    plt.plot(m,nFrame,'go', lw=2)
    plt.pause(1)
