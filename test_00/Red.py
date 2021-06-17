# -*- coding: utf-8 -*-
import os
import numpy as np
import random
import colorsys
import cv2

from mrcnn.config import Config
from mrcnn import model as modellib

#modelo pre-entrenado
model_filename = "mask_rcnn_object_0020.h5"
#clases correspondientes a modelo
class_names = ['BG','root']
min_confidence = 0.6

# Metodo de entrada
#camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("v001.mp4")
#camera = cv2.VideoCapture("Mapeo2.mp4")



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
    BACKBONE = 'resnet50'

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
assert model_path != "", "Provide path to trained weights"
#print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)



#Ciclo de ejecucion para entrada de video

#Ciclo de ejecucion B
cap = cv2.VideoCapture(1)
#camera = cv2.VideoCapture("v001.mp4")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # verificacion de lectura de frame, si ret es true (ok)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
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

        if label =='root':
            # Identificar Label
            print ( label,'root', class_id, 'class_ids')

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
            # convert the grayscale image to binary image
            ret,thresh = cv2.threshold(gray_image,0,255,0)


            #recorrido de matriz pxp
            for y in range(len(thresh)):
                for x in range(len(thresh[1,:])):
                    print('y: ',y, 'x: ',x,'Value: ',thresh[y,x])

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
            cv2.putText(frame_obj, "centroid", (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (139,0,0), 1)


            # depurar binarizacion
            #cv2.imshow('frame', thresh)   
            

    if N>0:
        cv2.imshow('frame', frame_obj)
    else:
        cv2.imshow('frame', frame)
    

    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()