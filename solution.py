# This is just a basic template for solution

from ast import While
from multiprocessing.connection import wait
from pickle import TRUE

from cv2 import destroyAllWindows, waitKey
import LRL_main_arena
import gym
import time
import pybullet as p
import cv2
import os
import numpy as np



def solve(b_low , b_high , gp_low , gp_high):
    i = 1
    j=0
    ander = 0
    previous_area = -1
    close_enough = 0
    flag=0

    vs = 7  #straight velocity
    vr = 6   #rotation velocity

    while True:
                       
        p.stepSimulation()                     

        
        img = env.get_camera_image()

        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, b_low ,b_high )
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        if len(contours) > 0:

            no_of_c = len(contours)

            cnt1= contours[no_of_c -1]
            M=cv2.moments(cnt1)

            area = cv2.contourArea(cnt1)

            if M['m00'] != 0:
                cx = int(M['m10']/(M['m00'] ))
                cy = int(M['m01']/(M['m00'] ))

                if cx >280 and cx < 320 :
                    env.move_husky(vs-2, vs-2, vs-2, vs-2)
                    env.open_husky_gripper()

                elif (cx < 280) :
                    env.move_husky(-vr, vr, -vr, vr)

                elif (cx > 320) :
                    env.move_husky(vr, -vr, vr, -vr)

                if(area >40000):
                    env.move_husky(0, 0,0 , 0)

                    while True:

                        env.close_husky_gripper()
                        
                        i=i+1
                        if (i>6):
                            env.move_husky(vr,-vr,vr ,-vr)
                            break
                        else:
                            env.move_husky(-vs, -vs,-vs , -vs)
                    break

        else:
            env.move_husky(vr, -vr, vr, -vr)

            
    while True:


#goalpost detection

                            p.stepSimulation()  

                            newimg = env.get_camera_image()
                            hsv = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)

                            mask = cv2.inRange(hsv,gp_low , gp_high )
                           
                            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                            no_of_c = len(contours)

                            if len(contours) > 0:

                                cnt= contours[no_of_c -1]
                                M=cv2.moments(cnt)
                                
                                area = cv2.contourArea(cnt)

                                if area > 30000:
                                    flag = 1

                                x,y,w,h = cv2.boundingRect(cnt)


                                if True:
                                    cx = x + (w/2)
                                    cy = y + (h/2)
                                    
                                   
                                    if(flag==1 and w<240):
                                        if(cx>330):
                                          env.move_husky(-vr, vr, -vr, vr)
                                        elif(cx<270):
                                          env.move_husky(vr, -vr, vr, -vr)
                                        else:
                                          env.move_husky(vs, vs, vs, vs)

                                    elif cx >= 285 and cx <=  315:
                                        env.move_husky(vs, vs, vs, vs)                                    
                                        ander = 1                                   

                                    elif (cx < 285) :
                                         env.move_husky(-vr+1, vr-1, -vr+1, vr-1)

                                    elif (cx > 315) :
                                         env.move_husky(vr-1, -vr+1, vr-1, -vr+1)

                                
                            elif ( len(contours)==0 and ander == 1):
                                    env.open_husky_gripper()
                                    env.move_husky(-vs, -vs, -vs, -vs)
                                    break

                            else:
                                env.move_husky(vr, -vr, vr, -vr)   

                        

    while True:

        p.stepSimulation()

        img = env.get_camera_image()
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv,  gp_low , gp_high )
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        if len(contours) > 0:

            cnt= contours[len(contours)-1]
            area = cv2.contourArea(cnt)

            if ( area > 32000) :
                env.move_husky(0, 0, 0, 0)
                break




if __name__ == '__main__':
    parent_path = os.path.dirname(os.getcwd()) # This line is to switch the directories for getting resources.
    os.chdir(parent_path)                      # you don't need to change anything in here.    

    env = gym.make("la_robo_liga_arena-v0")    # This loads the arena.

    pink_b_low = np.array([155, 100,100])
    pink_b_high = np.array([165, 135, 255])

    blue_b_low = np.array([80, 100,100])
    blue_b_high = np.array([100, 255, 255])

    yellow_b_low = np.array([25, 80,80])
    yellow_b_high = np.array([35, 200, 200])

    orange_b_low = np.array([10, 100,100])
    orange_b_high = np.array([25, 255, 255])


    pink_gp_low =  np.array([140, 135,100])
    pink_gp_high = np.array([160, 255, 255])

    blue_gp_low =  np.array([100, 100,100])
    blue_gp_high = np.array([145, 255, 255])

    yellow_gp_low =  np.array([25, 150,120])
    yellow_gp_high = np.array([35, 255, 255])

    orange_gp_low =  np.array([0, 100,160])
    orange_gp_high = np.array([9, 255, 255])

    solve(blue_b_low , blue_b_high , blue_gp_low , blue_gp_high)
    solve(yellow_b_low , yellow_b_high , yellow_gp_low , yellow_gp_high)
    solve(orange_b_low , orange_b_high , orange_gp_low , orange_gp_high)
    solve(pink_b_low , pink_b_high , pink_gp_low , pink_gp_high)
