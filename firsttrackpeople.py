import cv2
import mediapipe as mp
import numpy as np
cam = cv2.VideoCapture(0) #video cap
mp_drawing = mp.solutions.drawing_utils
pose = mp.solutions.pose
angle = []  
def calculate_angle(a, b, c):
    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle
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
        try:
            landmarks = result.pose_landmarks.landmark
            shoulder = [landmarks[pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[pose.PoseLandmark.RIGHT_WRIST.value].y]

            ang = calculate_angle(shoulder, elbow, wrist)
            text_position = (int(elbow[0] * frame.shape[1]), int(elbow[1] * frame.shape[0]))
            cv2.putText(image, f"salute: {ang:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                        cv2.LINE_AA)
            
            #logic
            if ang <=55 and ang >=40 :
                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(240, 155, 112), thickness=2, circle_radius=2),
                                   mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
            else:
                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(240, 155, 112), thickness=2, circle_radius=2),
                                   mp_drawing.DrawingSpec(color=(112, 112, 240), thickness=2, circle_radius=2))
        except AttributeError:
            pass

        #mp_drawing.draw_landmarks(image, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                                  # mp_drawing.DrawingSpec(color=(240, 155, 112), thickness=2, circle_radius=2),
                                 #  mp_drawing.DrawingSpec(color=(112, 112, 240), thickness=2, circle_radius=2))
        cv2.imshow('frame', image)

        if cv2.waitKey(1) == ord('0'):
            break

cam.release()
cv2.destroyAllWindows()

#mp_draw = mp.solutions.drawing_utils
#post_draw = mp.solutions.post