# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 22:33:46 2018

@author: Lagolas
"""

import numpy as np
import scipy
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from sklearn import mixture
import pickle
import os
from . import mfeatures
import warnings
warnings.filterwarnings("ignore")
import pyaudio
import wave

def test():
    print(os.listdir)
    #module_dir = os.path.dirname(__file__)  
    source = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\development_set\\'
    print(os.listdir)
    #source   = "\\development_set"   
    #module_dir = os.path.dirname(__file__) 
    modelpath = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\models' 
    #os.chdir('./streamapp/speech/')
    #print(os.listdir)

    os.makedirs(os.path.dirname(modelpath), exist_ok=True)
    os.makedirs(os.path.dirname(source), exist_ok=True)
    gmm_files = [os.path.join(modelpath,fname) for fname in 
                  os.listdir(modelpath) if fname.endswith('.gmm')]
    
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
    # Read the test directory and get the list of test audio files 
      
    #os.chdir('./myapp/speech/')
    module_dir = os.path.dirname(__file__)  
    path = source +'test.wav'
    #os.chdir('.\\myapp\\speech\\development_set')
    #print (os.listdir())
    #path="test.wav"
    rate,sig = wav.read(path)
    mfcc_feat=mfeatures.extract_features(sig,rate)
        
    log_likelihood = np.zeros(len(models)) 
        
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(mfcc_feat))
        log_likelihood[i] = scores.sum()
        print(speakers[i]+str(log_likelihood[i]))
    winner = np.argmax(log_likelihood)
    print ("\tdetected as - ", speakers[winner])
    os.chdir('..')
    os.chdir('..')
    print("HELPPPPPPPPPPPPPPPPPPP")
    print (os.listdir())
    return speakers[winner]
