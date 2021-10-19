## Creacion de entorno
    $ conda create -n AutoNav anaconda python=3.7.7
    $ conda activate AutoNav
    $ conda install tensorflow-gpu==2.1.0 cudatoolkit=10.1
    $ pip install tensorflow==2.1.0
    $ pip install keras
    $ pip install numpy scipy Pillow cython matplotlib scikit-image opencv-python h5py imgaug IPython[all]
    
## Instalar MaskRCNN (https://github.com/matterport)
    $ python setup.py install

## Uso de pycocotools
    $ pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI

# Repositorios Base
    Matterport, Inc
    https://github.com/matterport

    DavidReveloLuna
   https://github.com/DavidReveloLuna/MaskRCNN_Video 