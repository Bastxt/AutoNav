vData = VideoReader("vData\v001.mp4");
while hasFrame(vData)
    frame = readFrame(vData);
    C = semanticseg(frame,net);
    B = labeloverlay(frame,C);
    image(B)
    currAxes.Visible = 'off';
    pause(0.10/vData.FrameRate);
end