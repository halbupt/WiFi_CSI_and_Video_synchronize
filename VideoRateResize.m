function imgR = VideoRateResize(imgout,FrameRate)
% imgout is cell with the size m*n*number per-second 
% FrameRate is Video acquisition rate
numFrames = size(imgout,1);  % The total number of frames
T = round(numFrames/FrameRate);  %the number of frames as extraction interval
i = 1;
imgR = cell(FrameRate,1);
% with the expected interval to slelect the frame to save
 for k = 1:T:numFrames
     numframe = imgout{k};
     imgR {i} = numframe;     
     if i == FrameRate
         break;
     end
     i = i + 1;
 end
end