# -*- coding: utf-8 -*-
"""
@author: GENESIS
"""
import numpy as np
import scipy
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from sklearn import mixture
import pickle
import os
import warnings
from . import mfeatures
from django.core.files.storage import FileSystemStorage
warnings.filterwarnings("ignore")


def traine(x):
    file_paths=open("development_set_enroll.txt" ,'w')
    i=1
    #while i<2:
    file_paths.write(str(x) + str(i)+".wav\n")
    i+=1
    file_paths.close()
    #module_dir = os.path.dirname(__file__)  
    source = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\media\\' 
    #module_dir = os.path.dirname(__file__)  
    dest = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\models\\'
    #module_dir = os.path.dirname(__file__)  
    train_file = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\development_set_enroll.txt'    
    file_paths = open(train_file,'r')
    
    count = 1
    # Extracting features for each speaker (5 files per speakers)
    features = np.asarray(())
    for path in file_paths:    
        path = path.strip()
        # read the audio
        rate,sig = wav.read(source+path)
        mfcc_feat=mfeatures.extract_features(sig,rate)
        # extract MFCC 
        
        if features.size == 0:
            features = mfcc_feat
        else:
            features = np.vstack((features, mfcc_feat))
        # when features of 5 files of speaker are concatenated, then do model training
        if count >= 0:    
            gmm = mixture.GaussianMixture(n_components = 16, covariance_type='diag',n_init = 10)
            gmm.fit(features)
            
            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            print(picklefile)
            print(gmm)
            os.makedirs(os.path.dirname(dest+picklefile), exist_ok=True)
            pickle.dump(gmm,open(dest + picklefile,'wb'))
            #fs = FileSystemStorage(location='./models')
            #fs.save(picklefile, gmm, 'wb')
            features = np.asarray(())
            count = 0
        count = count + 1

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
