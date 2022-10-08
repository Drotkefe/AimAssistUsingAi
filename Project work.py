import time
import math
from turtle import distance, width
import win32api
import keyboard
import cv2
import mss
import numpy as np
import torch

def Closest_enemy(list):
    pos=win32api.GetCursorPos()
    distance=[]
    
    for i in list:
        width=i[2]-i[0]
        height=i[3]-i[1]
        center=(i[2]-width/2,i[3]-height/2)
        distance.append(math.sqrt((center[0]-pos[0])**2+(center[1]-pos[1])**2))
    return min(distance,default=0)
    

model=torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/Patrik/Desktop/best.pt')

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 960, "height": 540}

while True:
    img=np.array(sct.grab(monitor))
    result=model(img)
    rl=result.xyxy[0].tolist()
    #print(Closest_enemy(rl))
    #print(win32api.GetCursorPos())
    center=()
    if len(rl)>0:
        if rl[0][5]==1:
            distance=Closest_enemy(rl)
            width=rl[2]-rl[0]
            height=rl[3]-rl[1]
            center=(int(rl[2]-width/2),int(rl[3]-height/2))
            #laci=cv2.line(np.squeeze(result.render()),win32api.GetCursorPos(),center,color=(0,255,0),thickness=3)
            #cv2.imshow('sad',laci)
        else if()
            
    cv2.imshow('debug',np.squeeze(result.render()))
    cv2.waitKey(1)
    if keyboard.is_pressed('q'):
        break
cv2.destroyAllWindows()

    
