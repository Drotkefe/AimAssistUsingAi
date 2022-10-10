import time
import math
import win32api
import keyboard
import cv2
import mss
import numpy as np
import torch
import random

def Closest_enemy_head(list):
    pos=win32api.GetCursorPos()
    centers=[]
    distance=[]
    for i in list:
        if i[5]==1:
            width=i[2]-i[0]
            height=i[3]-i[1]
            center=(i[2]-width/2,i[3]-height/2)
            centers.append(center)
            distance.append(math.sqrt((center[0]-pos[0])**2+(center[1]-pos[1])**2))
    if len(centers)==0:
        return
    return centers[distance.index(min(distance,default=None))]

def Closest_enemy(list):
    pos=win32api.GetCursorPos()
    centers=[]
    distance=[]
    for i in list:
        if i[5]==0 and i[4]>0.7:
            width=i[2]-i[0]
            height=i[3]-i[1]
            center=(i[2]-width/2,i[3]-height/2)
            centers.append(center)
            distance.append(math.sqrt((center[0]-pos[0])**2+(center[1]-pos[1])**2))
    if len(centers)==0:
        return
    return centers[distance.index(min(distance,default=None))]


def cursor_move(x,y):
    pos=win32api.GetCursorPos()
    while(pos[0]!=x and pos[1]!=y): 
        vector=(x-pos[0],y-pos[1])
        x_dist=vector[0]//random.randint(7,20)
        y_dist=vector[1]//random.randint(8,14)
        win32api.mouse_event(0x0001,x_dist,y_dist)
        pos=win32api.GetCursorPos()
        time.sleep(abs(x_dist/1000))
    


model=torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/Patrik/Desktop/best.pt')

with mss.mss() as sct:
    #monitor = {"top": 225, "left": 450, "width": 1020, "height": 630}
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
while True:
    t1 = time.time()
    img=np.array(sct.grab(monitor))
    cv2.circle(img,(960,540),5,(255,0,0),-1)
    result=model(img)
    rl=result.xyxy[0].tolist()
    if len(rl)>0:
        mouse_loc=win32api.GetCursorPos()
        dest=Closest_enemy_head(rl)
        print(dest)
        if dest==None:
            dest=Closest_enemy(rl)
        else:
            cursor_move(int(dest[0]),int(dest[1]))  
    t2 = time.time()
    times=[]
    times.append(t2-t1)
    times = times[-50:]
    ms = sum(times)/len(times)*1000
    fps = 1000 / ms
    print("FPS", fps)
    cv2.circle(img,(500,600),50,(255,0,0),-1)
    cv2.imshow('debug',np.squeeze(result.render()),)
    cv2.waitKey(1)
    
    if keyboard.is_pressed('q'):
        break
cv2.destroyAllWindows()

    
