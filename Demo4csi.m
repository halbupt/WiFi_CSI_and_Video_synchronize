% ---Yanling
% Extract the CSI
%% read the csi
%
% clc; clear;
addpath('csitoolbox');
% addpath(genpath('.'));

GI = 1; % Guradinterval, if it's 0,it's 0.8us,if 1, it's 0.4us
dir = 'D:\DATA\YL_0306_csidata\1c113packet\packet1k-dun';% load CSI directory
cdir1 = strcat(dir,'\log_yanling.dat');
cdir2 = strcat(dir,'\time_yanling.txt');
sdir = 'C:\Users\Yanling\Documents\1_Human_Pose_Estimation\data\preparedata\examples\wifiposedata\scene1_without_occlusion\person1_female\act000000_squating\csi_res\';% save CSI directory

% ------- read CSi_trace
csi_trace = read_bf_file(cdir1);
% csi_trace(cellfun(@isempty,csi_trace))=[]; %remove the empety elements,
% to avoid the situation, try to stop the receriver with ctrl+c in the terminal% 

%% calculate te expected number of the csi from the timestamp.txt
% [H, M, S] = textread(cdir2,'%n %n %f','delimiter', ':'); % load the timestamp

Timestring = textread(cdir2,'%s');% load the timestamp
csi_HMS = datevec(Timestring,'HH:MM:SS.FFF');

csi_HMS(:,2) = 3;  %set the month
csi_HMS(:,3) = 6; %set the day

H = csi_HMS(:,4);
M = csi_HMS(:,5);
S = csi_HMS(:,6);

sum_len1 = uint32((S(end)-S(1)+(M(end)-M(1))*60+(H(end)-H(1))*3600)*100); %timestamp to count the number of csi sample


% calculate te expected number of the csi from the timestamp_low
len = size(csi_trace,1);
sum_time = csi_trace{len}.timestamp_low-csi_trace{1}.timestamp_low;
sum_len2 = uint32 (sum_time./10000); %the timestamp_low to count the number of csi sample,100Hz--100 samples per sencon,0.01*10^9=100000000 

sum_len = max(sum_len1,sum_len2);%choose the large to ensure all the number

%% Mean imputation

csi_matrix = zeros (3, 3, 30, sum_len);%the whole reshaped matrix 

k = 1;
for t= 1:len-1 
    csi_entry = get_scaled_csi(csi_trace{t});%extract the csi matrix    
    
    
    
    csi_matrix (:,:,:,k) = csi_entry;%copy to the matrix   
    
    if sum_len1 ~= sum_len2
        if (csi_trace{t+1}.timestamp_low - csi_trace{t}.timestamp_low) > 1000000  
            % linear interpolation
            csi_left = get_scaled_csi(csi_trace{t});
            csi_right = get_scaled_csi(csi_trace{t+1});
            for j=1:30
                csi_new(:,:,j) = (csi_left(:,:,j)+csi_right(:,:,j))/2;
            end              
            k = k+1; 
            csi_matrix(:,:,:,k) = csi_new; %python is opposite like (t,:,:,:)     
        end
        
        k = k+1;
        
        if k >sum_len2
           print('too many interpolation')
        end
    end
    
end

csi_s = permute (csi_matrix,[4,3,1,2]);

%% Save the CSI [3 x 3 x 30 x sum_number] to a sequnence in the format of [5 x 30 x 3 x 3]

sn= floor(len/5); 
for s=1:sn
    csi_serial = csi_s((5*s-4):s*5,:,:,:);
    sdir1=strcat(sdir,num2str(s),'.mat');
    save(sdir1,'csi_serial');    
end


%% convert the date string to Unix time, to be compared with the video in
% order to sychronize.
csi_datestr1 = datestr(csi_HMS(1,:,:,:,:,:));
csi_datetime1 = datetime(csi_datestr1);
csi_unixT1 = posixtime(csi_datetime1);% csi start time

csi_datestr2 = datestr(csi_HMS(sn*5,:,:,:,:,:));
csi_datetime2 = datetime(csi_datestr2);
csi_unixT2 = posixtime(csi_datetime2);% csi end time, posixtime calcultates the seconds in Unix format

edir = strcat(sdir,'\csi_unixT.xls');
xlswrite(edir,[csi_unixT1,csi_unixT2]);% save the unixT as excel

rmpath('\csitoolbox');



