import time
import math
from turtle import distance, width
import win32api
import keyboard
import cv2
import mss
import numpy as np
import torch

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
    return centers[distance.index(min(distance,default=None))]


sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5) 
def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            #move_mouse(current_x:=move_x,current_y:=move_y)
            win32api.mouse_event(0x0001,move_x,move_y)
    #return current_x,current_y
    


model=torch.hub.load('ultralytics/yolov5','custom',path='C:/Users/Patrik/Desktop/best.pt')

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 960, "height": 540}

while True:
    img=np.array(sct.grab(monitor))
    result=model(img)
    rl=result.xyxy[0].tolist()
    center=()
    if len(rl)>0:
        # width=rl[2]-rl[0]
        # height=rl[3]-rl[1]
        # center=(int(rl[2]-width/2),int(rl[3]-height/2))
        # mouse_loc=win32api.GetCursorPos()
        print(Closest_enemy_head(rl))
        
        #wind_mouse(mouse_loc[0],mouse_loc[1],center[0],center[1])
            # distance=Closest_enemy(rl)
            #laci=cv2.line(np.squeeze(result.render()),win32api.GetCursorPos(),center,color=(0,255,0),thickness=3)
            #cv2.imshow('sad',laci)
    time.sleep(1.5)
    cv2.imshow('debug',np.squeeze(result.render()))
    cv2.waitKey(1)
    if keyboard.is_pressed('q'):
        break
cv2.destroyAllWindows()

    
