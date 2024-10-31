import cv2
import mediapipe as mp
import numpy as np
cam = cv2.VideoCapture(0) #video cap
mp_drawing = mp.solutions.drawing_utils
pose = mp.solutions.pose
with pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose_model:
    if not cam.isOpened():
        print("Cannot open cam")

    while True : 
        ret,frame = cam.read()
        
        #color cam track
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        result = pose_model.process(frame)
        #print(result)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try :
            landmarks = result.pose.landmarks
        except :
            pass
        mp_drawing.draw_landmarks(image, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
        #print(result.pose_landmarks)
            mp_drawing.DrawingSpec(color=(240,155,112), thickness =2, circle_radius =2),    #circle
            mp_drawing.DrawingSpec(color=(112,112,240), thickness =2, circle_radius =2))     #line
        def callculateang(a,b,c): #first f(x)
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            
            
        cv2.imshow('frame', image)


        if cv2.waitKey(1) == ord('0'):
            break

cam.release()
cv2.destroyAllWindows()

#mp_draw = mp.solutions.drawing_utils
#post_draw = mp.solutions.post
