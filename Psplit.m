function [train_data, train_label,test_data, test_label] = Psplit(train_d,label_t,scene,person,flag)
% split all the sample  
%flag 1 for 'proportion', 2 for person1 train& person3 test, 2.5 opposite, 3 for scene 1&2 train, scene3 test                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              


if flag ==1
    num_sample = size(train_d,1); % find the number of samples for each action
    % split by propotion
    % training & testing data split as 7:3
    num_train = floor(num_sample*0.7);  % set the split number of train sample for each action
    x = train_d(1:num_train,:,:,:,:);  % train_d:[num*30*3*3*200]
    y = label_t(1:num_train);
    
    x_l = train_d(num_train+1:end,:,:,:,:);
    y_l = label_t(num_train+1:end);
    
elseif flag == 2   % person 1 train, person 3 test
    num_p = person;
    if num_p == 1% person 1-->train
        x = train_d;
        y = label_t;
    else
        x_l= train_d;
        y_l = label_t;
    end
    
elseif flag == 2.5   % person 1 train, person 3 test
    num_p = person;
    if num_p == 3% person 3-->train
        x= train_d;
        y = label_t;
    else
        x_l= train_d;
        y_l = label_t;
    end
    
elseif flag ==3  % scene 1&2 train, scene 3 test
    num_p = scene;
    if num_p == 1 || num_p == 2% scene 1&2 -->train
        x= train_d;
        y = label_t;
    else
        x_l= train_d;
        y_l = label_t;
    end
    
end

train_data = x;% [num*270*200]
train_label = y;
test_data = x_l;
test_label = y_l;
end