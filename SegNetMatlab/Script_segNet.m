[imds,pxds] = pixelLabelTrainingData(gTruth);

%Ajuste de peso para clases
tbl = countEachLabel(pxds)
totalNumberOfPixels = sum(tbl.PixelCount);
frequency = tbl.PixelCount / totalNumberOfPixels;
classWeights = 1./frequency

    
numFilters = 64;
filterSize = 3;
numClasses = 6;
%%
layers = [
    imageInputLayer([1080 1920 3])
    convolution2dLayer(filterSize,numFilters,'Padding',1)
    reluLayer()
    maxPooling2dLayer(2,'Stride',2)
    convolution2dLayer(filterSize,numFilters,'Padding',1)
    reluLayer()
    transposedConv2dLayer(4,numFilters,'Stride',2,'Cropping',1);
    convolution2dLayer(1,numClasses);
    softmaxLayer()
    pixelClassificationLayer('Classes',tbl.Name,'ClassWeights',classWeights);
    ];

opts = trainingOptions('sgdm', ...
    'InitialLearnRate',1e-3, ...
    'MaxEpochs',60, ...
    'MiniBatchSize',64, ...
    'Plots','training-progress');
trainingData = pixelLabelImageDatastore(imds,pxds);
net = trainNetwork(trainingData,layers,opts);