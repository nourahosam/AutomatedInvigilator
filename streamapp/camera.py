import dlib
import cv2
import argparse, os, random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import datasets, transforms
import pandas as pd
import numpy as np
from .model import model_static
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from colour import Color
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from datetime import datetime

class VideoCamera(object):
    def __init__(self,userr):
        self.cap = cv2.VideoCapture(0)
        self.user = userr
        print("init")
    def __del__(self):
        self.cap.release()


    def bbox_jitter(bbox_left, bbox_top, bbox_right, bbox_bottom):
        cx = (bbox_right+bbox_left)/2.0
        cy = (bbox_bottom+bbox_top)/2.0
        scale = random.uniform(0.8, 1.2)
        bbox_right = (bbox_right-cx)*scale + cx
        bbox_left = (bbox_left-cx)*scale + cx
        bbox_top = (bbox_top-cy)*scale + cy
        bbox_bottom = (bbox_bottom-cy)*scale + cy
        return bbox_left, bbox_top, bbox_right, bbox_bottom



    def get_frame(self):
        print("run")
        # set up vis settings
        model_weight = 'D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Invigilator\\myapp\\data\\model_weights.pkl'
        jitter = 0
        red = Color("red")
        colors = list(red.range_to(Color("green"),10))
        font = ImageFont.truetype("data/arial.ttf", 40)
        vis = False
        display_off = False
        save_text = False

        # set up video source

        video_path = 'live.avi'
        #ret, frame = self.cap.read()


        # set up face detection mode

        facemode = 'DLIB'

        if facemode == 'DLIB':
            detector = dlib.get_frontal_face_detector()
        frame_cnt = 0

        # set up data transformation
        test_transforms = transforms.Compose([transforms.Resize(224), transforms.CenterCrop(224), transforms.ToTensor(),
                                            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        # load model weights
        model = model_static(model_weight)

        model.cuda()
        model.train(False)
        looking = 0
        notlooking = 0
        # video reading loop

        print("helpppppppppppppppppppppppppppppp")
        ret, frame = self.cap.read()
		#successs,jpeg = cv2.imencode('.jpg', np.array(frame))
        if ret == True:
            height, width, channels = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame_cnt += 1
            bbox = []
            if facemode == 'DLIB':
                dets = detector(frame)
                for d in dets:
                    l = d.left()
                    r = d.right()
                    t = d.top()
                    b = d.bottom()
                    # expand a bit
                    l -= (r-l)*0.2
                    r += (r-l)*0.2
                    t -= (b-t)*0.2
                    b += (b-t)*0.2
                    bbox.append([l,t,r,b])
        
            frame = Image.fromarray(frame)
            for b in bbox:
                face = frame.crop((b))
                img = test_transforms(face)
                img.unsqueeze_(0)
                if jitter > 0:
                    for i in range(jitter):
                        bj_left, bj_top, bj_right, bj_bottom = self.bbox_jitter(b[0], b[1], b[2], b[3])
                        bj = [bj_left, bj_top, bj_right, bj_bottom]
                        facej = frame.crop((bj))
                        img_jittered = test_transforms(facej)
                        img_jittered.unsqueeze_(0)
                        img = torch.cat([img, img_jittered])

                # forward pass
                output = model(img.cuda())
                if jitter > 0:
                    output = torch.mean(output, 0)
                score = F.sigmoid(output).item()
                coloridx = min(int(round(score*10)),9)
                draw = ImageDraw.Draw(frame)
                draw.text((b[0],b[3]), str(round(score,2)), fill=(255,255,255,128), font=font)
                module_dir = os.path.dirname(__file__)  
                file_path = os.path.join(module_dir, 'log.txt') 
                file_object = open(file_path, 'a')

                if(round(score) > 0.3):
                    print("score:", str(round(score,2)))
                    looking +=1
                else:
                    print("Not looking")
                    notlooking +=1
                print("LOOOKING:", looking)
                print("NOT LOOKING", notlooking)
                accuracy = (notlooking/(notlooking+looking))*100
                #accuracy = (notlooking/(notlooking+looking))*100
                print("Accuracy: ", accuracy)

                if(score >0.2):
                    now = datetime.now()
    
                    print("now =", self.user)

                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    #print("date and time =", dt_string)
                    dt_string = dt_string + ' FOCUSED \n'
                    file_object.write(dt_string)
                else:
                    now = datetime.now()
    
                    print("now =", self.user)

                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    #print("date and time =", dt_string)
                    dt_string = dt_string + ' CHEATING \n'
                    file_object.write(dt_string)
                    file_object.close()
            successs,jpeg = cv2.imencode('.jpg', np.array(frame))
            
            return jpeg.tobytes()
                
