#Import all important functionality
import cv2
import mediapipe as mp
import serial
import time

# Open sPort
sPort=serial.Serial('/dev/ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
print("Wait for Arduino to recover from reset...")
time.sleep(2)
sPort.write(str.encode('<2,0,2>'))

#Start cv2 video capturing through CSI port
cap=cv2.VideoCapture(2)

#Initialise Media Pipe Pose features
mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
pose=mp_pose.Pose()

#Start endless loop to create video frame by frame Add details about video size and image post-processing to better identify bodies
while True:
    ret,frame=cap.read()
    flipped=cv2.flip(frame,flipCode=1)
    frame1 = cv2.resize(flipped,(640,480))
    rgb_img=cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
    result=pose.process(rgb_img)
    #Print general details about observed body
    #print (result.pose_landmarks)
    
    #Uncomment below to see X,Y coordinate Details on single location in this case the Nose Location.
    #XC = (mp_pose.PoseLandmark.NOSE.x * 640)
    #YC = (mp_pose.PoseLandmark.NOSE.y * 480)
    
    

   
    try:        
 
    
     xPos = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * 640)
     yPos = int(result.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * 480)
     
     print('Rounded X is: ',xPos)
     print('Rounded Y is: ',yPos)
     margin=20;
     
     #Check X aim
     if (xPos > (320+margin)):
         #Move left
         print('Move left!')
         sPort.write(str.encode('h'))
         
     elif (xPos < (320-margin)):
         #Move right
         print('Move right!')
         
         sPort.write(str.encode('H'))
     else:
         print("X is close enough!")
         sPort.write(str.encode('j'))
     
     #Check Y aim
     if (yPos > (220+margin)):
         #Move left
         print('Move down!')
         sPort.write(str.encode('V'))
         
     elif (yPos < (220-margin)):
         #Move right
         print('Move up!')
         sPort.write(str.encode('v'))
         
     else:
         print("Y is close enough!")
         sPort.write(str.encode('s'))
 
     # Check if within range for both X and Y
     if ((320 - margin) <= xPos <= (320 + margin)) and ((220 - margin) <= yPos <= (220 + margin)):
         print('Go!')
         sPort.write(str.encode('FR'))
     else:
         print("Moving!")
         sPort.write(str.encode('fO')) 
    
 
    except:
        print("NO TARGET")
        sPort.write(str.encode('esB'))

  
    
    #Draw the framework of body onto the processed image and then show it in the preview window
    mpDraw.draw_landmarks(frame1,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
    cv2.imshow("frame",frame1)
    
    #At any point if the | q | is pressed on the keyboard then the system will stop
    key = cv2.waitKey(1) & 0xFF
    if key ==ord("q"):
        break
        
