function [train_data,test_data]= Preshape(train_data,train_label,test_data,test_label,action_seg)

seg= action_seg*100;

train_data_reshape = zeros([length(train_label),30*3*3*seg]);% ----------SET 1s for 270
test_data_reshape = zeros([length(test_label),30*3*3*seg]);% ----------SET


for i = 1:length(train_label)
    temp = squeeze(train_data(i,:,:,:,:));
    train_data_reshape(i,:) = temp(:);
end

for i = 1:length(test_label)
    temp = squeeze(test_data(i,:,:,:,:));
    test_data_reshape(i,:) = temp(:);
end


% train_data_reshape = train_data_reshape';
% test_data_reshape = test_data_reshape';

train_data = train_data_reshape;
test_data  = test_data_reshape;

end