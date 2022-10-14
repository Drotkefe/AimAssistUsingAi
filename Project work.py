import time
import math
import win32api
import keyboard
import cv2
import mss
import numpy as np
import torch
import random
import pyautogui
from win32gui import FindWindow, GetWindowRect



def get_window_geometry(name):
    window_handle = FindWindow(None, name)
    window_rect   = GetWindowRect(window_handle)
    return window_rect

x, y, w, h=get_window_geometry("Counter-Strike: Global Offensive - Direct3D 9") #cs-re

def Closest_enemy_head(list):
    centers=[]
    distance=[]
    for i in list:
        if i[5]==1 and i[4]>0.4:
            width=i[2]-i[0]
            height=i[3]-i[1]
            center=(int(i[2]-width/2),int(i[3]-height/2))
            centers.append(center)
            distance.append(math.sqrt((center[0]-w/2)**2+(center[1]-h/2)**2))
    if len(centers)==0:
        return
    print("fejlövés")
    return centers[distance.index(min(distance,default=None))]

def Closest_enemy(list):
    centers=[]
    distance=[]
    for i in list:
        if i[5]==0 and i[4]>0.7:
            width=i[2]-i[0]
            height=i[3]-i[1]
            center=(int(i[2]-width/2),int(i[3]-height/2))
            centers.append(center)
            distance.append(math.sqrt((center[0]-w/2)**2+(center[1]-h/2)**2))
    if len(centers)==0:
        return
    return centers[distance.index(min(distance,default=None))]

    
if torch.cuda.is_available():
    print(torch.cuda.get_device_properties(0).name)
else:
    print("nincs neked")
torch.zeros(1).cuda()


model=torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/Patrik/Desktop/best.pt')
sct=mss.mss()
#monitor = {"top": 225, "left": 450, "width": 1020, "height": 630}


while True:
    last_time = time.time()
    img=np.array(sct.grab({"top": y, "left": x, "width": w, "height": h,"mon":-1})) #cs-re
    #img=np.array(sct.grab({"top": 0, "left": 0, "width": 1920, "height": 1080,"mon":-1}))
    result=model(img)
    rl=result.xyxy[0].tolist()
    if len(rl)>0:
        dest=Closest_enemy_head(rl)
        diff_x=0
        diff_y=0
        if dest!=None:
            diff_x=(int(dest[0])-int(w/2))
            diff_y=(int(dest[1])-int(h/2))
            win32api.mouse_event(0x0001,int(diff_x),diff_y)
        else:
            dest=Closest_enemy(rl)
            if dest!=None:
               diff_x=(int(w/2)-int(dest[0]))*-1
               diff_y=(int(h/2)-int(dest[1]))*-1
               win32api.mouse_event(0x0001,int(diff_x),diff_y)

    print("fps: {}".format(1 / (time.time() - last_time)))
    cv2.imshow('debug',np.squeeze(result.render()))
    cv2.waitKey(1)
    


    
