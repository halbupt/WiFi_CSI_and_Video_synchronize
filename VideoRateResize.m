function imgR = VideoRateResize(imgout,FrameRate)
% imgout is cell with the size m*n*number per-second 
% FrameRate is Video acquisition rate
numFrames = size(imgout,1);  % The total number of frames
% T = round(numFrames/FrameRate);  %the number of frames as extraction interval
% T = floor(numFrames/FrameRate);

T = 3;
wantframe = 30;% assumed there is no lost frame it is 30, but in fact sometimes is less than 30
% with the expected interval to slelect the frame to save
N = (wantframe-numFrames)-floor((wantframe-numFrames)/3);% the number of lost frames to be added

for k = 1:T:numFrames-N*3 % how to add the lost frame? only by reducing the loop frame in every three frames
    
    imgout{k}=[];    
end  
 
 imgout(cellfun(@isempty,imgout))=[];
 
 i = 1;
 imgR = cell(FrameRate,1);
 for j =1:FrameRate 
     imgR{i} = imgout{j}; 
     if i == FrameRate
         break;
     end
     i = i + 1;
 end
end