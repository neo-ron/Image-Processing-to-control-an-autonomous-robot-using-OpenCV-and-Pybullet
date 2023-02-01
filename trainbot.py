import imp
from multiprocessing.connection import wait
from numpy import arctan
from pyparsing import matchOnlyAtCol
from gym_line_follower.helper import LaRoboLigaEnv
import math
import time


if __name__ == "__main__":
    husky = LaRoboLigaEnv()
    
    #full path co-ordinates
    mypath = husky.get_full_path()

    i=1

    while i < len(mypath)  :

     #husky.set_velocity([0, 0])

     while True:
        #required yaw
        rotation_angle = math.atan2(( mypath[i][1] - husky.get_position()['y']) , (mypath[i][0] - husky.get_position()['x']))
        pos =husky.get_position()['yaw']
        

        #to check if path foward is fairly straight
        if i < len (mypath) -30:
          far_angle = math.atan2(( mypath[i+30][1] - mypath[i-1][1]) , (mypath[i +30][0] - mypath[i -1][0]))

        #to increase speed if path is straight
        if  abs(far_angle - husky.get_position()['yaw']) < 0.1:
          velocity = 1.2
        else:
          velocity = 0.6
       

        #if yaw and rotation angle are close enough, then move foward
        if (rotation_angle - 0.02) < pos and pos < (rotation_angle + 0.02) :
            husky.set_velocity([0,0])
            
            while True: 
                 if (mypath[i][1]-0.05< husky.get_position()['y'] and husky.get_position()['y'] < mypath[i][1]+0.05) and (mypath[i][0]-0.05 < husky.get_position()['x'] and husky.get_position()['x'] < mypath[i][0]+0.05):
                   husky.set_velocity([0.0,0.0])
                   break

                 else :
                   husky.set_velocity([velocity,velocity])
                   
            break
      
      #to align husky in direction of the rotation angle
        else :
          #for the abrubt jump from pi to -pi 
            if (pos > 0 and rotation_angle < -3):
              husky.set_velocity([-0.08,0.08])

            elif (pos < 0 and rotation_angle > 3):
              husky.set_velocity([0.08,-0.08])
             
            elif(pos>rotation_angle):
             husky.set_velocity([0.08,-0.08])
        
            else :
             husky.set_velocity([-0.08,0.08])
             

      #to see how much path is completed   
     #print( str(i) + "/" + str(len(mypath)))

     i=i+5
   

    print("\nTrack Completed!\nRobo Club OP!\n")
            
              



        