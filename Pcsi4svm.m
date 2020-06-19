function [train_data,label_data]=Pcsi4svm(csi_amp,scene,person,action,action_seg)
% For python SVM test for each person in each scene
addpath(genpath('.'));

name_action = strcat(num2str(scene),'_',num2str(person),'_');  

name_dir = strcat('Result\svmtrain_single_',num2str(action_seg),'s');
mkdir(name_dir);
seg = action_seg*100;


nind = action; %female 1:11;male 1:6,9:11%    
  
sum_len = length(csi_amp);
sn = (sum_len - rem(sum_len,seg))/seg;% avoid the index exceed the max
%     train_o= zeros(30,3,3,seg,sn);
%     train_g = zeros(seg,30,3,3);%100 packet for 1s as an action
for s=1:sn
    csi_mat = csi_amp;
    train_g = csi_mat((seg*s-seg+1):s*seg,:,:,:);
    train_s =  permute(train_g, [2,3,4,1]);
    train_o(:,:,:,:,s)= train_s;
end
train_d = permute(train_o, [5,1,2,3,4]);%(sn,30,3,3,seg)
save([name_dir,'\train_data\','train_data_',name_action, num2str(nind),'_', num2str(sn),'.mat'], 'train_d');

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
save([name_dir,'\train_label\','train_label_',name_action, num2str(nind),'_', num2str(sn),'.mat'], 'label_t');

train_data =train_d;
label_data =label_t;

end
    
