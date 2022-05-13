# WiFi and Video Sychronize 

A.  Installation MATLAB Engine API for python

    ----Windows
     cd "matlabroot\extern\engines\python"
     python setup.py install

    ----Mac or Linux
     cd "matlabroot/extern/engines/python"
     python setup.py install

    * 如果创建python有venv目录（自己建的虚拟环境，一般Anaconda 的envs中），此目录下包含着该项目的依赖文件。需要将build目录matlabroot\extern\engines\python\matlab 复制到venv\Lib目录下。



B.  Datasets Downloads from https://drive.google.com/file/d/16V_NFY0YV_ouXGfO7hvZtNEG4sBl2a2D/view?usp=sharing
                 
     put it into the directory as '*/WiFi_CSI_and_Video_synchronize/examples/*'
     
     All method 2 in readCSI.py directly use the csi_amplitude that is in '*/examples/wifiposedata/scene1_without_occlusion/person1_female/act000001_falling_down/csi_res'
        
   
C. (1) Demosvm.py for SVM classification.the datasets downloads from https://drive.google.com/file/d/1pME9TcA8YXjD5n4kgD3Ft9B069AfI6bm/view?usp=sharing

              put it into the directory as '*/WiFi_CSI_and_Video_synchronize/Result/*'
              
   (2) Demoforcsinet.py for CSInet classification.

D.   explainations

(1).ReadCSI.py--python function directly processing the raw CSI *.dat into the reqiured training datasets for all algorithmn

All method 2 in readCSI.py directly use the csi_amplitude that is in '*/examples/wifiposedata/scene1_without_occlusion/person1_female/act000001_falling_down/csi_res'

    use : [train_data,train_label,test_data,test_label] = ReadCSI.csi4svm (month,day,scene,person,action,action_seg,split_flag, objflag)
  
          1）month day - the csi data captured
  
          2）scene - 1 for without occlusion， 2  for partial occlusion，3 for fullocclusion
  
          3）person - 1 for female， 3 for male
  
          4）action -[1,2,3,4,5,6,9,10,11] are "falling_down", "throwing", "pushing", "kicking", "punching","jumping", "drinking","phone_talking", "seating", here we move action 10 11     into action 7,8 in process.
  
          5）actionseg - second(s) for an action
  
          6）split_flag - 1 for 'proportion'[ default as 70% for training,30% for testing]; 2 for person1 train & person3 test; 2.5 person3 train & person1 test; 3 for scene 1&2 train, scene3 test
          
          7) objflag- 'SVM' 'csinet' 'LSTM'
  

（2）.PDemo4csi.m--matlab function extract csi amplitudes and phase from raw csi *.dat
     use :
   
     import matlab.engine 
    
     eng = matlab.engine.start_matlab()
  
     [csi_amp, csi_pha] = eng.PDemo4csi(month,day,scene,person,action,nargout = 2),nargout is the number of the output parameters
  
  

（3）.Csi4actseg.py--function segment csi amplitude into action by time     
  
（4）.Split.py--function split training data by proportion,person,scene.


# Copyright 
if you use this code please refer :
Hao, Y., et al. (2020). A Wireless-Vision Dataset for Privacy Preserving Human Activity Recognition. 2020 Fourth International Conference on Multimedia Computing, Networking and Applications (MCNA).
    

