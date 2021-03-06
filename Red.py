# -*- coding: utf-8 -*-
import os
import numpy as np
import random
import colorsys
import cv2
import imutils
import math

import lib.graph as gp

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.pylab import *

from mrcnn.config import Config
from mrcnn import model as modellib

#modelo pre-entrenado
model_filename = "red101_80.h5"
#clases correspondientes a modelo
#class_names = ['BG','root']
class_names = ['BG','Floor']
min_confidence = 0.6
disArr=[]

# Metodo de entrada
#camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("v001.mp4")
#camera = cv2.VideoCapture("Mapeo2.mp4")


#conteo de fotogramas
fps = 0
#media
m = np.array([0.1])
m[0] = 0

#variables de orientacion punto Objetivo
nFrame = np.array([0.1])
trackpoint = np.array([0.1])
###########################################################

#clase de configuracion para modelo de inferencia
class SetNetConfig(Config):
    # Give the configuration a recognizable name
    NAME = "SetNet"

    # Train on 1 GPU and 1 image per GPU. Batch size is 1 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # background + 1 (casco)

    # All of our training images are 512x512
    IMAGE_MIN_DIM = 256
    IMAGE_MAX_DIM = 256

    # You can experiment with this number to see if it improves training
    STEPS_PER_EPOCH = 500

    # This is how often validation is run. If you are using too much hard drive space
    # on saved models (in the MODEL_DIR), try making this value larger.
    VALIDATION_STEPS = 5
    
    # Matterport originally used resnet101, but I downsized to fit it on my graphics card
    BACKBONE = 'resnet101'

    # To be honest, I haven't taken the time to figure out what these do
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 32
    MAX_GT_INSTANCES = 50 
    POST_NMS_ROIS_INFERENCE = 500 
    POST_NMS_ROIS_TRAINING = 1000 
    
config = SetNetConfig()
config.display()

#modelo de inferencia
class InferenceConfig(SetNetConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 256
    IMAGE_MAX_DIM = 256
    DETECTION_MIN_CONFIDENCE = min_confidence
    

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", config=inference_config,  model_dir='logs')

# Obtener .h5 con los pesos de la red entrenada
model_path = os.path.join('logs', model_filename)

#se puede obtener el ultimo modelo del directorio model_dir
#model_path = model.find_last()

# Cargar pesos de modelo .h5 pre-entrenado
assert model_path != "", "Archivo no encontrado"
#print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)



#Ciclo de ejecucion para entrada de video

#Ciclo de ejecucion B
#cap = cv2.VideoCapture(0) #Selecciond de dispositivo de entrada
cap = cv2.VideoCapture('Mapeo2.mp4')
ret, frame = cap.read()
old_gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
lk_params= dict(winSize = (640,480), 
                maxLevel=2,
                criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10,0.03))
primPos=0
#camera = cv2.VideoCapture("v001.mpexit()4")

#definicion de graficas

fig = plt.figure(num = 0, figsize = (10, 30))#, dpi = 100)
fig.suptitle("Posicion de punto objetivo vs FPS", fontsize=12)
ax01 = subplot2grid((1, 1), (0, 0))
ax01.set_xlim(0,600)
plt.ion()
plt.show()
#ax02 = subplot2grid((3, 2), (0, 1))
#ax03 = subplot2grid((3, 2), (1, 0))
#ax04 = subplot2grid((3, 2), (1, 1))
#ax05 = subplot2grid((3, 2), (2, 0), colspan=2, rowspan=1)

############################################################


if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    #old_gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # verificacion de lectura de frame, si ret es true (ok)
    if not ret:
        print("Error frame...")
        break
    
    # pos-proceso frame a frame
    
    #redimensionar imagen
    frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
    #frame = cv2.resize(frame, (940, 780), interpolation = cv2.INTER_AREA)
    #frame = cv2.resize(frame, (1080, 1920), interpolation = cv2.INTER_AREA)
    
    #aplicar modelo de inferencia al frame actual
    results = model.detect([frame], verbose=0)
    r = results[0]
    #print('RESULTADOS ----',r)
    N =  r['rois'].shape[0]     #obtener capas detectadas
    boxes=r['rois']             #obtener contenedor
    masks=r['masks']            #mascara detectada
    class_ids=r['class_ids']    #id de clase actual
    scores=r['scores']          #score de deteccion
    
    # Definir escala de colores    
    #hsv = [(i / N, 1, 0.7) for i in range(N)]
    #colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    
    #random.shuffle(colors)
    #print("N_obj:",N)
    

    for i in range(N):
        #print(N)
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        
        class_id = class_ids[i]                             # Obtener id de clase
        score = scores[i] if scores is not None else None   # Separar Score
        label = class_names[class_id]                       # Separar nombre de clase

        #if label =='root':
        if label =='Floor':
            # Identificar Label
            #print ( label,'Floor', class_id, 'class_ids')

            #capturar frame en codificacion requerida
            masked_image = frame.astype(np.uint32).copy()

            color = (80,255,51) #definir color
            #ajuste de opacidad 
            alpha=0.5
             
            # Obtener capa detectada
            mask = masks[:, :, i]
            #imagen base(lienzo)
            image = np.zeros((480, 640, 3), np.uint8)


            # definir mascara super puesta a imagen
            for c in range(3):
                masked_image[:, :, c] = np.where(mask == 1,
                                    masked_image[:, :, c] *
                                    (1 - alpha) + alpha * color[1],
                                    masked_image[:, :, c])
            
            # definir mascara dummy
            for c in range(3):
                image[:, :, c] = np.where(mask == 1,
                                    image[:, :, c] *
                                    (1 - alpha) + alpha * color[1],
                                    image[:, :, c])


            #Obtener Centroide
            gray_image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            gray_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # convert the grayscale image to binary image
            ret,thresh = cv2.threshold(gray_image.astype(np.uint8),0,255,0)
            
            
            # find contours in thresholded image, then grab the largest
            # one
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            #img, contours, hierarchy = cv2.findContours(imageCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)

            #cv2.drawContours(image, [c], -1, (0, 255, 255), 2)           
            #for x in range(len(c[1,:])):
            #    print('y: ',y, 'x: ',x,'Value: ',thresh[y,x])



            #extA = tuple(c[0,:][0])
            #extB = tuple(c[2,:][0])
            #extC = tuple(c[3,:][0])
            #extD = tuple(c[4,:][0])

            # calcular momentos 
            M = cv2.moments(thresh)
            
            # calcular coordenadas
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])        
                

            # normalizacion de capa a formato uint8
            frame_obj=masked_image.astype(np.uint8)
            #obtener contenedores de secciones detectadas
            #y1, x1, y2, x2 = boxes[i]
            #Marca de seguimiento para seccion detectada
            #cv2.rectangle(frame_obj, (x1, y1), (x2, y2),color, 2)  
            
            # Definicion de tecto para recuadro
            #caption = "{} {:.3f}".format(label, score) if score else label

            # Agregar titulo a a marca de seguimiento 
            #cv2.putText(frame_obj,caption,(int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Agregar Marca de centroide
            cv2.circle(frame_obj, (cX, cY), 5, (139,0,0), -1)
            #cv2.putText(frame_obj, "centroid", (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
            cv2.putText(frame_obj, str((cX, cY)), (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
            #Dibuja el contorno detectado
            cv2.line(frame_obj, (0, cY), (640, cY), (0, 0, 255),1)
            cv2.line(frame_obj, (cX+50, 480), (cX+50,0), (0, 0, 255),1)
            cv2.line(frame_obj, (cX-50, 480), (cX-50,0), (0, 0, 255),1)
            cv2.drawContours(frame_obj, [c], -1,(169, 35, 180), 2)
             #recorrido de matriz pxp
            disArr=[] 
            ##la idea con este for (for y in range(len(c)):) es recorrer la imagen por primera vez y sacar un array de las distancias de cada punto del contorno vs el centroide.
            for y in range(len(c)):
                ext = tuple(c[y][0])
                #print('tama??o: ',len(c[y,:]))
                if ext[1]<cY:               
                    #cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                    #cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1) #Trazar posible linea entre el punto del controno y el centroide
                    #print( 'Eje x : ',ext[0],'Eje y : ',ext[1], cX,cY)
                    #Pitagoras para sacar magnitud y distancia entre 2 puntos
                    #d(A,B)= sqrt((x2-x1)^2 +(y2-y1)^2)         
                    # En este Array (dis) vamos al almacenar  [distancia desde el centroide al punto del contorno, coordenada (x,y) del punto del contorno, coordenada (x,y) del centro de la imagen recorrida]           
                    dis=[round(math.sqrt(pow(((ext[1])-(cY)),2)+pow(((ext[0])-(cX)),2))),(ext),(cX,cY)]
                    #print(dis)
                    disArr.append(dis)
                    dis=[]
            disArr.sort(reverse=True)
            #print('IMPRIMI----------------------------------------------------------------',disArr)
            posDisArr=0
            countDis=0
            codis=0
            disArrCorY=[]
            disArrCorX=[]
            ## Este for se encarga de recorrer el array disArr que tiene las distancias ordenadas de mayor a menor.
            for t in range(len(disArr)): 
                centro=disArr[posDisArr][2]
                posCont=disArr[posDisArr][1]
                distancia=disArr[posDisArr][0]
                ##  Este if se hizo con el fin de almacena rla primera posicion la mas lejana, y en el else se almacena las siguiente 5 teniendo un margen de 10 entre cada una, solamente se almacenan 6 (codis)
                if countDis ==0: 
                    ## Aca se esta seleccionando los puntos que esten arriba del centroide con el fin de tener todas las distancias de la parte delantera                                                                                             
                    if posCont[1]< centro[1] :
                        #print('-CENTRO-',centro,'POSICION',posDisArr)
                        #print('-CONTORNO-',posCont,'POSICION',posDisArr)    
                        #print('-PASE EL PRIMER IF 1 POSICION----------------',centro,'centro restado|',(centro[0]-50),'|PUNTO A COMPARAR|',posCont[0],'|centro sumado',(centro[0]+50))
                        ## En este if se establecio un margen simulando un angulo de 45 grados a cada lado, pero en base a la la resta de cierta cantidad (50) a la coordenada x con el fin de generar el abanico.
                        if (posCont[0] < (centro[0]+50)) and (posCont[0] > (centro[0]-50)):
                            disArrCorY.append(posCont[1])
                            disArrCorX.append(posCont[0])
                            ##Como en este for no se tiene el tuple del for anterior(for y in range(len(c)):), pero si se tiene la informacion almacenada en dissArr[1] que es el punto del contorno donde se tomo dicha distancia se iguala a ext para poder hacer el punto sobre la mascara
                            ext=(posCont[0],posCont[1]) 
                            #salida de posicion seleccionada
                            #print('Posicion: ',ext)
                            #gafica de puntos sobre eje ax01
                            ax01.plot(posCont[0],fps,'bo', lw=2)
                            trackpoint = np.append(trackpoint,[posCont[0]])
                            nFrame = np.append(nFrame,[fps])
                            
                            m = np.append(m,[sum(trackpoint)/len(trackpoint)])
                            ax01.plot(m,nFrame,'go', lw=2)

                            ##Este se encarga de poner el punto donde va el contorno.                                                       
                            cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                            #Este se encarga de poner en texto las coordenadas (x,y)del punto del contorno.
                            cv2.putText(frame_obj,str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                            #Este se encarga de trazar la linea desde el centro al punto del contorno escogido
                            cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1) 
                            ext=()
                            disAnt=distancia
                            countDis+=1       
                            codis+=1                                 
                
                else:
                    if codis < 6:                        
                        if posCont[1]< centro[1] :
                            #print('-CENTRO-',centro,'POSICION',posDisArr)
                            #print('-CONTORNO-',posCont,'POSICION',posDisArr) 
                            #print('-PASE EL PRIMER IF 2 POSICION----------------',centro,'|centro restado',(centro[0]-50),'|PUNTO A COMPARAR',posCont[0],'|centro sumado',(centro[0]+50))
                            if (posCont[0] < (centro[0]+50)) and (posCont[0] > (centro[0]-50)):
                                if (disAnt-distancia) >10:
                                    disArrCorY.append(posCont[1])
                                    disArrCorX.append(posCont[0])
                                    ext=(posCont[0],posCont[1])                                    
                                    #cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                                    #cv2.putText(frame_obj,str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                                    #cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1) 
                                    
                                    disAnt=distancia
                                    codis+=1                       
                posDisArr+=1
            disArr=[]
            #disArrCorY=[disArr[0][1],disArr[1][1],disArr[2][1],disArr[3][1],disArr[4][1],disArr[5][1],disArr[6][1],disArr[7][1],disArr[8][1],disArr[9][1],disArr[10][1],disArr[11][1],disArr[12][1],disArr[13][1],disArr[14][1],disArr[15][1],disArr[16][1],disArr[17][1],disArr[18][1],disArr[19][1],disArr[20][1]]
            #disArrCorX=[disArr[0][2],disArr[1][2],disArr[2][2],disArr[3][2],disArr[4][2],disArr[5][2],disArr[6][2],disArr[7][2],disArr[8][2],disArr[9][2],disArr[10][2],disArr[11][2],disArr[12][2],disArr[13][2],disArr[14][2],disArr[15][2],disArr[16][2],disArr[17][2],disArr[18][2],disArr[19][2],disArr[20][2]]
            #
            #print('-----------Array Y--------',disArrCorY)
            #print('-----------Array X----------',disArrCorX)            
            disant=0            
            """for y in range(len(c)):                                        
                ext = tuple(c[y][0])                           
                if ext[1]<cY:
                    #print('------Begin-----')
                    #print(range(len(c)))        
                    try:
                        #print(disArrCorX,'-- valor guardado vs valor corriendo xxxxx--',ext[0])
                        #print(disArrCorY,'-- valor guardado vs valor corriendo yyyyy--',ext[1])
                        vectorx=pow((ext[0]-cX),2)
                        vectory=pow((ext[1]-cY),2)
                        valArrX=disArrCorX.index(ext[0])
                        valArrY=disArrCorY.index(ext[1])
                        #print(valArrX,'----',type(valArrX))
                        #print(valArrY,'----',type(valArrY))
                        if valArrY == valArrX:                                                                                        
                            punto=round(math.sqrt(vectorx+vectory))
                            disant=punto
                            print(ext,'ext')                            
                            print(valArrY,'valArrY')
                            print(valArrX,'valArrX')
                            cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                            #cv2.putText(frame_obj,str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                            cv2.putText(frame_obj,str(punto)+'--'+str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)                                       
                            cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1)                                                                                   
                    except Exception as e:
                        #print('Ha ocurrido un error debido a',e)
                        var=e
                    
                countIma+=1 """                  
                #print('------End-----',countIma)
            disArrCorY=[]
            disArrCorX=[]

            """for t in range(len(disArr)):
                    #if  count == 10 or count == 50 or count == 100 or count == 150 or count == 200 or count == 280 or count == 300 or count == 350 or count == 400 or count == 415 or count == 420:
                    if ext[1]<cY:
                        if countDis ==0: 
                            countDis+=1
                            vectorx=pow((ext[0]-cX),2)
                            vectory=pow((ext[1]-cY),2)                                     
                            punto=round(math.sqrt(vectorx+vectory))
                            disant=punto
                            codis+=1
                            print(punto,'count 0')
                            cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                            #cv2.putText(frame_obj,str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                            cv2.putText(frame_obj,str(punto)+'--'+str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)                                       
                            cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1)
                            break
                        else:
                            if codis < 6:
                                vectorx=pow((ext[0]-cX),2)
                                vectory=pow((ext[1]-cY),2)                                                                  
                                punto=round(math.sqrt(vectorx+vectory))
                                disVal=disant-70
                                if disVal<= punto:
                                    print(punto,'codis : ',codis)
                                    cv2.circle(frame_obj, ext, 3, (0, 0, 255), -1)
                                    #cv2.putText(frame_obj,str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                                    cv2.putText(frame_obj,str(punto)+'--'+str(ext),ext,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)
                                    #cv2.putText(frame_obj, str(punto), ext, cv2.FONT_HERSHEY_SIMPLEX, fontScale,color, thickness, cv2.LINE_AA, True)                                                                                               
                                    cv2.line(frame_obj, (cX, cY), ext, (255, 0, 0),1)
                                    codis+=1 
                                    break"""
                     
                

            #print('Contador---------------',count)
            # depurar binarizacion
            #cv2.imshow('frame', thresh)   
            

    if N>0:
        cv2.imshow('frame', frame_obj)
    else:
        cv2.imshow('frame', frame_obj)

    #Graficar Resultados
    fps+=1
    ############################################################
    

    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()