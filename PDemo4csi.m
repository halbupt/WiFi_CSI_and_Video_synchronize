function [csi_amplitude, csi_phase]= PDemo4csi(month,day,scene,person,action)
% Extract the CSI amplitude and phase from the raw csi.dat---Yanling
%csi_amplitude:[num*30*3*3], csi_phase:[num*30*3*3]
% month =3 day =24
%% read the csi
% clc; clear;
% add all the sub directory;
addpath(genpath('.'));
if scene == 1
    s='scene1_without_occlusion';
elseif scene == 2
    s='scene2_partial_occlusion';
elseif scene == 3
    s='scene3_full_occlusion';
end

if person == 1
    p='person1_female';
elseif person == 3
    p='person3_male';
end

directory = strcat('examples\wifiposedata\',s,'\',p,'\');% load CSI directory
subdir = dir(directory);%find all the action data,but start at 2ed.
name_action = strcat(num2str(scene),'_',num2str(person),'_');

% GI = 1; % Guradinterval, if it's 0,it's 0.8us,if 1, it's 0.4us

nind = action; %female 1:11;male 1:6,9:11%--------------------------------------------set

cdir1 = strcat(directory,subdir(nind+2).name,'\csi\log_yanling.dat');
cdir2 = strcat(directory,subdir(nind+2).name,'\csi\time_yanling.txt');
% check wether the file exists

if ~exist(cdir1,'file')||~exist(cdir2,'file')
    disp('Lack of the *.dat or *.txt files') 
    csi_amplitude = 0;
    csi_phase = 0;
    return 
else
    % mkdir to save CSI 
    sdir = strcat(directory,subdir(nind+2).name,'\csi_res\');
    if ~exist(sdir,'dir')
       mkdir(sdir);
    end
    % ------- read CSi_trace
    csi_trace = read_bf_file(cdir1);
    % csi_trace(cellfun(@isempty,csi_trace))=[]; %remove the empety elements,
    % to avoid the situation, try to stop the receriver with ctrl+c in the terminal%
    
    %% calculate te expected number of the csi from the timestamp.txt
    % [H, M, S] = textread(cdir2,'%n %n %f','delimiter', ':'); % load the timestamp
    
    Timestring = textread(cdir2,'%s');% load the timestamp
    csi_HMS = datevec(Timestring,'HH:MM:SS.FFF');
    
    %
    csi_HMS(:,2) = month;  % the month 3
    csi_HMS(:,3) = day; % the day 24
    %
    H = csi_HMS(:,4);
    M = csi_HMS(:,5);
    S = csi_HMS(:,6);
    
    sum_len1 = uint32((S(end)-S(1)+(M(end)-M(1))*60+(H(end)-H(1))*3600)*100); %timestamp to count the number of csi sample
    
    
    % calculate te expected number of the csi from the timestamp_low
    %--first to figure whether there are lost packets . if linear, it's normal
    len = size(csi_trace,1);
%     for tt=1:len
%         Time_low{tt} = csi_trace{tt}.timestamp_low;
%     end
%     Time_stamp = cell2mat(Time_low);%draw the time interval to see whether there are packets loss
%     figure;
%     plot(Time_stamp);
%     pause(1);
%     close;
    %--then calculate the number of the csi
    sum_time = csi_trace{end}.timestamp_low-csi_trace{1}.timestamp_low;
    sum_len2 = uint32 (sum_time./10000); %the timestamp_low to count the number of csi sample,100Hz--100 samples per sencon,0.01*10^6=10000?s
    
    sum_len = max(sum_len1,sum_len2);%choose the large to ensure the max number
    
    
    %% Mean imputation
    csi_ampmat = zeros (3, 3, 30, sum_len);%the whole reshaped matrix
    csi_phamat = zeros (3, 3, 30, sum_len);
    k = 1;
    for t= 1:len-1
        csi_entry = get_scaled_csi(csi_trace{t});%extract the csi matrix
        
%         csi_amp = db(abs(csi_entry));%get the Amplitude of complex Numbers as Amplitude ---change db
        csi_amp = abs(csi_entry);
        csi_pha = angle(csi_entry); % --------------------------------------------------add phase
        
        csi_ampmat (:,:,:,k) = csi_amp;%copy to the matrix
        csi_phamat (:,:,:,k)=  csi_pha;
        
        if sum_len ~= len
            if (csi_trace{t+1}.timestamp_low - csi_trace{t}.timestamp_low) > 10000  %wrong
                % linear interpolation for amp &pha
                csi_entryleft = get_scaled_csi(csi_trace{t});
                csi_entryrigh = get_scaled_csi(csi_trace{t+1});
                
                csi_ampleft = db(abs(csi_entryleft));
                csi_amprigh = db(abs(csi_entryrigh));
                
                csi_phaleft = angle(csi_entryleft);
                csi_pharigh = angle(csi_entryrigh);
                
                for j=1:30
                    csi_ampnew(:,:,j) = (csi_ampleft(:,:,j)+csi_amprigh(:,:,j))/2;
                    csi_phanew(:,:,j) = (csi_phaleft(:,:,j)+csi_pharigh(:,:,j))/2;
                end
                k = k+1;
                csi_ampmat(:,:,:,k) = csi_ampnew; %python is opposite like (t,:,:,:)
                csi_phamat(:,:,:,k) = csi_phanew;
            end
            
            %         if k >sum_len2
            %            print('too many interpolation')
            %            break;
            %         end
        end
        k = k+1;
    end
    
    csi_amps = permute (csi_ampmat,[4,3,1,2]);% the saved format[num*30*3*3]
    csi_phas = permute (csi_phamat,[4,3,1,2]);
    
    csi_amplitude = csi_amps;
    csi_phase = csi_phas;
    save(strcat(sdir,name_action,num2str(nind),'_amp.mat'), 'csi_amps') ;% save the amp & phase mat
    save(strcat(sdir,name_action,num2str(nind),'_pha.mat'), 'csi_phas') ;
    
    
%     %% For WiSPPN---Save the CSI [3 x 3 x 30 x sum_number] to a sequnence in the format of [5 x 30 x 3 x 3]
%     numname = 6;   %the length of image name
%     nz = strcat('%0',num2str(numname),'d'); % '%06d'
%     f = 1;
%     % sn= floor(sum_len/5);
%     sn = (sum_len - rem(sum_len,5))/5;% avoid the index exceed the max
%     for s=1:sn
%         csi_serial = csi_amps((5*s-4):s*5,:,:,:);
%         namecsi = sprintf(nz,f);
%         save(strcat(sdir,namecsi,'.mat'), 'csi_serial') ;
%         f = f+1;
%         %     sdir1=strcat(sdir,num2str(s),'.mat');
%         %     save(sdir1,'csi_serial');
%     end
%     
%     %% sychronize time with video---convert the date string to Unix time, to be compared with the video in
%     % order to sychronize.
%     csi_datestr1 = datestr(csi_HMS(1,:,:,:,:,:));
%     csi_datetime1 = datetime(csi_datestr1);
%     csi_unixT1 = posixtime(csi_datetime1);% csi start time
%     
%     
%     % csi_datestr2 = datestr(csi_HMS(sn*5,:,:,:,:,:));
%     % csi_datetime2 = datetime(csi_datestr2);
%     % csi_unixT2 = posixtime(csi_datetime2);% csi end time, posixtime calcultates the seconds in Unix format
%     csi_unixT2 = csi_unixT1 + sn*5*0.01;
%     
%     edir = strcat(sdir,'\csi_unixT.xls');
%     xlswrite(edir,[csi_unixT1,csi_unixT2]);% save the unixT as excel
end
rmpath(genpath('.'));
end



