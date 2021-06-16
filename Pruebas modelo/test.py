import numpy as np

A = np.matrix([[1,2,0],[3,4,0],[5,6,0]])
B = np.matrix([[9],[8],[0]])

# [12,34,0.5]

C = np.matrix([[1,0,0],[0,1,0],[0,0,1]])
X = np.matrix([[8],[2],[3]])


print(C.dot(X))


# por cada vuelta (cada segundo)
#x = lidar(90)
#y = lidar(0)
#theta = ((vD-vI)/l)