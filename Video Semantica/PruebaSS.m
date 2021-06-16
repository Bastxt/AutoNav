%%Prueba Semantica



% 
% I = readimage(imds,1);
% figure
% imshow(I)
% obj = VideoReader('Mapeo2.mp4');
% vid = read(obj);
% imwrite(vid(:,:,10,:),strcat('frame-',num2str,'.png'));
% frames = obj.NumberOfFrames;
% for x = 1 : frames
%     imwrite(vid(:,:,:,x),strcat('frame-',num2str(x),'.png'));
% end
%% Comandos que ayudan a generar frames especificos, usarlo cuando se usa la herramienta VideoLabel. 
% ReadObj = VideoReader('Mapeo2.mp4'); 
% CurFrame = 0;
% GetFrame = [1 3 4 9 23 34 40 43 44 49 51 52 74 101 104 113 116 123 124 164 178 214 294 339 373 400 449 467 500 533 573 608 640 673 701 724 736 772 802 859 860 861 862 863 864 865 866 867 868 869 870 871 882 907 971 1002 1031 1072 1107 1133 1135 1160 1188 1189 1190 1191 1192];
% while hasFrame(ReadObj)
%     CurImage = readFrame(ReadObj);
%     CurFrame = CurFrame+1;
%     if ismember(CurFrame, GetFrame)
%         imwrite(CurImage, sprintf('frame%d.jpg', CurFrame));
%     end
% end


classNames = ["Floor" "Pared" "Puerta" "Obstaculo" "Silla" "Mueble"];
pixelLabelID = [1 2 3 4 5 6];
imDir = fullfile(pwd,'Images');
pxDir = fullfile(pwd,'PixelLabelData');

 imds = imageDatastore(imDir);
%I = readimage(imds,28);
% figure
%%imshow(I)


pxds = pixelLabelDatastore(pxDir,classNames,pixelLabelID);

% C = readimage(pxds,28);
% B = labeloverlay(I,C);
%%imshow(B)
tbl = countEachLabel(pxds)

%[imdsTrain, imdsVal, imdsTest, pxdsTrain, pxdsVal, pxdsTest] = partitionCamVidData(imds,pxds);
% buildingMask = C == 'Pared';
% figure
% imshowpair(I, buildingMask,'montage')

numFilters = 1080;
filterSize = 3;
numClasses = 6;
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
    pixelClassificationLayer()
    ]

opts = trainingOptions('sgdm', ...
    'InitialLearnRate',1e-3, ...
    'MaxEpochs',100, ...
    'MiniBatchSize',12);

trainingData = pixelLabelImageDatastore(imds,pxds);


net = trainNetwork(trainingData,layers,opts);