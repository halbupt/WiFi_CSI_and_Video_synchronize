function [train_data,label_data]=Pcsi4actseg(csi_amp,scene,person,action,action_seg)
% CSI segmentation for an action, all save in 'Result/actionseg_*/'
addpath(genpath('.'));

name_action = strcat(num2str(scene),'_',num2str(person),'_');  

name_dir = strcat('Result\actionseg_',num2str(action_seg),'s');
s_dir1 = strcat(name_dir,'\train_data');
s_dir2 = strcat(name_dir,'\train_label');

if ~exist(name_dir,'dir')
    mkdir(name_dir);    
end
if ~exist(s_dir1,'dir')
    mkdir(s_dir1);    
end
if ~exist(s_dir2,'dir')
    mkdir(s_dir2);    
end

seg = action_seg*100;% the number of csi packages for an action


nind = action; %female 1:11;male 1:6,9:11%    
  
sum_len = length(csi_amp);
sn = (sum_len - rem(sum_len,seg))/seg;% avoid the index exceed the max
    train_o= zeros(30,3,3,seg,sn);
    train_g = zeros(seg,30,3,3);% an action csi serial
for s=1:sn
    csi_mat = csi_amp;
    train_g = csi_mat((seg*s-seg+1):s*seg,:,:,:);
    train_s =  permute(train_g, [2,3,4,1]);
    train_o(:,:,:,:,s)= train_s;
end

train_d = permute(train_o, [5,1,2,3,4]);%(sn,30,3,3,seg)
save([s_dir1,'\train_data_',name_action, num2str(nind),'_', num2str(sn),'.mat'], 'train_d');

% writing the corresponding the label. Due to we lack action 7, 8, so
% we move 10, 11 ahead
if nind == 10
    label = 7;
elseif nind == 11
    label = 8;
else
    label = double(nind) ;
end

label_t = ones (sn,1)*label;
save([s_dir2,'\train_label_',name_action, num2str(nind),'_', num2str(sn),'.mat'], 'label_t');

train_data =train_d;
label_data =label_t;

end
    
