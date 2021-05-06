% ---Yanling
% Read the ROSBag messgage recorded by the D435i, including the depth ,
% color and the motion frames.

clear;
clc;
vdir = 'E:\DATA\YL_0324_videodata\scene3\ZY\';%%--------------------------------------------set
vbag = dir([vdir,'*.bag']);%
% vdir = dir (dir);

directory = 'examples\wifiposedata\scene3_full_occlusion\person3_male\';%--------------------------------------------set
subdir = dir(directory);%find all the action data,but start at 2ed.
name_action = '3_3_';%need to revise,first:scene,second person,third action--------------------------------------------set

% for nind = 1:6
for nind = 9:length(subdir)-2
    
    sdir = strcat(directory,subdir(nind+2).name,'\frame\');%
    
    if length(vbag)== length(subdir)-2
        bag = rosbag([vdir, vbag(nind).name]);% accroding the video bag
    else
        if nind <7
            bag = rosbag([vdir, vbag(nind).name]);% accroding the video bag
        else
            bag = rosbag([vdir, vbag(nind-2).name]);% female: nind; male:[1:6]-nind;[9:11]-nind-2
        end
        
    end
    
    FPS = 20; % desired FPS
    
    % use select function to narrow the selection of messages
    % ---choose the time to narrow %
    csi_unixT = xlsread([directory,subdir(nind+2).name,'\csi_res\csi_unixT.xls']);%check the timestamp with the CSI
    video_elapse =  csi_unixT (2)-csi_unixT (1);% the elapse time according to the csi captured
    % ---sychronize time
    start = sychronize_time(bag,csi_unixT);
    
    % select the frames every second with the timestamp csi_unixT
    imgR = select_per_second(bag,start,video_elapse,FPS);
    
    % save all frame as seperate mat
    save_frame(sdir,name_action,nind,FPS,video_elapse,imgR);
    
end




function start = sychronize_time(bag,csi_unixT)
% sychronize time
% ---chosse the topic to narrow
geometry_message = select(bag,'Topic','/device_0/sensor_0/Depth_0/image/data');%choose depth is because it is smaller than color to avoid the java error.
msgs = readMessages(geometry_message);

% find the closest time
len = size (msgs,1);
video_unixT = zeros(len,1);

% select all the frame timestamps
for i = 1:len
    video_unixT(i) = msgs{i}.Header.Stamp.Sec;
end

% use sort function to justify
[St, video_index] = sort (abs(video_unixT-csi_unixT(1)));
start = video_index(1)/len*(bag.EndTime - bag.StartTime)+ bag.StartTime;% according to the index to locate the starttime in video bag
end


function imgR = select_per_second(bag,start,video_elapse,FPS)
% select the frames every second with the timestamp csi_unixT
imgR = cell(video_elapse,1);
for e =1: video_elapse
    timecut_message = select(bag,'Time',[start+e-1 start+e],'Topic','/device_0/sensor_1/Color_0/image/data');
    timecut_msgs = readMessages(timecut_message);
    
    flag = 0;   % 0 for color & 1 for depth--------------------------------------------set
    
    if flag == 0 %--------if color
        imgout=cell(size(timecut_msgs,1),1);
        for j=1:size(timecut_msgs,1)
            [img,alpha] = readImage(timecut_msgs{j});
            writeImage(timecut_msgs{j},img);
            imgout{j}=img;
            clear img
        end
        imgR{e} = VideoRateResize(imgout,FPS);
        
    else %--------------if depth
        depthLim =1000; %remove all depth data greater than depthLim
        imgout=cell(size(timecut_msgs,1),1);
        for j= 1: size(timecut_msgs,1)
            [img,alpha] = readImage(timecut_msgs{j});
            writeImage(timecut_msgs{j},img);
            imgout{j}=img;
            clear img
        end
        imgR{e} = VideoRateResize(imgout,FPS);
    end
    
end
end


function save_frame(sdir,name_action,nind,FPS,video_elapse,imgR)
%save all frame as seperate mat
numname = 6;   %the length of image name
nz = strcat('%0',num2str(numname),'d'); % '%06d'
f = 1;
mkdir([sdir,name_action,num2str(nind)]);
for i =1:video_elapse
    for j= 1: FPS
        rframe = imgR{i}{j};
        frame = imresize(rframe, 0.5);
        nameFrame = sprintf(nz,f);   %i is saved the sequence number of the picture? it has format of ‘000001’
        imwrite(frame,strcat(sdir,name_action,num2str(nind),'\',nameFrame,'.jpg'),'jpg');%
        save(strcat(sdir,nameFrame,'.mat'), 'frame') ;
        f = f+1;
    end
    
end
end

