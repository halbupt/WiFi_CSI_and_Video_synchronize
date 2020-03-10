
clear;
% [x1,y1,c1,x2,y2,c2,x3,y3,c3]
% val.bodies(1).joints 

% video_name = 1:10; %10 videos
addpath(genpath('.'));

video_name = 1;
for name_index = video_name 

    directory = 'examples\wifiposedata\scene1_without_occlusion\person1_female\act000000_squating\';
    frame_files = dir([directory,'frame\','*.mat']);
    csi_files = dir([directory,'csi_res\','*.mat']);
    
    len = min (length(frame_files),length(csi_files));
    
    for i = 1:len
        % if only open number one
        if  isempty(strfind(frame_files(i).name, 'two'))&& isempty(strfind( frame_files(i).name, 'three'))&& ...
            isempty(strfind(frame_files(i).name, 'four'))&& isempty(strfind( frame_files(i).name, 'five'))
            
            % load coco-18
            fname = [directory, 'frame_alphapose_res\sep-json\', frame_files(i).name(1:end-4), '.json'];% the saved skeleton map as json
            if ~isempty(dir(fname))           
                               
                             
                
            fid = fopen(fname); 
            
            raw = fread(fid,inf); 
            str = char(raw'); 
            fclose(fid);  
                            
            
            
            val = jsondecode(str);
            joints = val.bodies(1).joints;
            
            x = joints(1:3:end);
            y = joints(2:3:end);
            c = joints(3:3:end);
            
            
            jointsVector = [x;y;c;c];
            
            jointsMatrix = zeros([18,18,4]);
            
            for row = 1:18
                for column = 1:18
                    if row == column
                        jointsMatrix(row,column,:) = [x(row),y(row),c(row),c(row)];
                    else
                        jointsMatrix(row,column,:) = [x(row)-x(column),y(row)-y(column),c(row)*c(column),c(row)*c(column)];
                    end 
                end
            end
            frame_files(i).name

            load([ frame_files(1).folder, '\',  frame_files(i).name], 'frame');
            load([ csi_files(1).folder, '\',  csi_files(i).name], 'csi_serial');
            save(['test_preparedata\', frame_files(i).name], 'csi_serial', 'frame', 'jointsVector', 'jointsMatrix', '-v7.3')
            end
        end  

    end
 
end

