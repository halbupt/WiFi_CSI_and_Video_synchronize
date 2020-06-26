# Yanling
Combined wireless signals and video for intelligent sensing

A.  Installation MATLAB Engine API for python

    ----Windows
     cd "matlabroot\extern\engines\python"
     python setup.py install

    ----Mac or Linux
     cd "matlabroot/extern/engines/python"
     python setup.py install

    * 如果创建python有venv目录（自己建的虚拟环境，一般Anaconda 的envs中），此目录下包含着该项目的依赖文件。需要将build目录matlabroot\extern\engines\python\matlab 复制到venv\Lib目录下。



B.  Datasets Downloads from https://drive.google.com/drive/folders/184qnT8qCyuw-lQy3cl0CQ_18dtfmK0_A?usp=sharing.
                 
     put it into the directory as '*/WiFi_CSI_and_Video_synchronize/examples/*'


C.   Run Demosvm for SVM classification.

D.   explainations

(1).ReadCSI.py--python function directly processing the raw CSI *.dat into the reqiured training datasets for SVM

    use : [train_data,train_label,test_data,test_label] = ReadCSI.csi4svm (month,day,scene,person,action,action_seg,split_flag)
  
          1）month day - the csi data captured
  
          2）scene - 1 for without occlusion， 2  for partial occlusion，3 for fullocclusion
  
          3）person - 1 for female， 3 for male
  
          4）action -[1,2,3,4,5,6,9,10,11] are "falling_down", "throwing", "pushing", "kicking", "punching","jumping", "drinking","phone_talking", "seating", here we move action 10 11     into action 7,8 in process.
  
          5）actionseg - second(s) for an action
  
          6）split_flag - 1 for 'proportion'[ default as 70% for training,30% for testing]; 2 for person1 train & person3 test; 2.5 person3 train & person1 test; 3 for scene 1&2 train, scene3 test
  

（2）.PDemo4csi--matlab function extract csi amplitudes and phase from raw csi *.dat
     use :
   
     import matlab.engine 
    
     eng = matlab.engine.start_matlab()
  
     [csi_amp, csi_pha] = eng.PDemo4csi(month,day,scene,person,action,nargout = 2),nargout is the number of the output parameters
  
  

（3）.Pcsi4actseg--matlab function segment csi amplitude into action by time
 
     use : [train, label] = eng.Pcsi4actseg(csi_amp, scene, person, action, action_seg, nargout = 2) 
  
  

（4）.Psplit--matlab function split training data by proportion,person,scene.

    use: [train_d, train_l, test_d, test_l] = eng.Psplit(train, label, scene, person, split_flag, nargout = 4) 

