# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 08:10:20 2021

@author: noura
"""

import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import warnings
import numpy as np
from sklearn import preprocessing
import mfeatures
import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn import mixture
import warnings
import time, os
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore")

dir = "data/Speaker1_digit_1/wav/"

spf = wave.open(dir + 'Speaker1_digit_1_0.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#Checking the number of input channels, current model is only for single channel
spf.getnchannels() 
print("haha")

plt.plot(signal)
plt.title('Signal Wave...')

#path to training data
source   = "data\\"   

#path where training speakers will be saved
dest = "models\\"
train_file = "development_set_enroll.txt"        
file_paths = open(train_file,'r')


count = 1
# Extracting features for each digit data provided by speaker 
features = np.asarray(())
for path in file_paths:    
    path = path.strip()   
    print(path)
    
    sr,audio = read(source + path)
    
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = mfeatures.extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of training files of each digit for a given speaker are concatenated, model training is done
    if count == 10:    
        gmm = mixture.GaussianMixture(n_components = 16, covariance_type='diag',n_init = 10)
        gmm.fit(features)
        
        # dumping the trained gaussian model
        picklefile = path.split("\\")[0]+".gmm"
        pickle.dump(gmm,open(dest + picklefile,'wb'))
        print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)    
        features = np.asarray(())
        count = 0
    count = count + 1

#path to training data
source   = "data\\"   
models_dir = "models\\"
test_file = "testing_list.txt"        
file_paths = open(test_file,'r')

gmm_files = [os.path.join(models_dir,fname) for fname in os.listdir(models_dir) if fname.endswith('.gmm')]

print(gmm_files)

#Load the Gaussian Models
models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
models

speakers_digit   = [fname.split("\\")[-1].split(".gmm")[0] for fname in gmm_files]
print(speakers_digit)

path_predicted_dict = dict()

for path in file_paths:   
    
    path = path.strip()   
    print(path)
    sr,audio = read(source + path)
    vector   = mfeatures.extract_features(audio,sr)
    
    log_likelihood = np.zeros(len(models)) 
    
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    
    winner = np.argmax(log_likelihood)
    print("\tSpeaker & Digit detected as - ", speakers_digit[winner])
    path_predicted_dict[path] = speakers_digit[winner]


correct_pred = 0
incorrect_pred = 0
for i in path_predicted_dict.keys():
    if i.split("\\")[0] == path_predicted_dict[i]:
        correct_pred += 1
    else:
        incorrect_pred += 1
 
print("Accuracy on Test Dataset = ", correct_pred*100/(correct_pred + incorrect_pred), "%")


