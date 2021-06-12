import mediapipe as mp
import cv2
import time
from directkeys import right_pressed,left_pressed
from directkeys import PressKey, ReleaseKey
import pygetwindow as gw

def right():
    PressKey(right_pressed)
    ReleaseKey(left_pressed)
    time.sleep(0.5)

def left():
    PressKey(left_pressed)
    ReleaseKey(right_pressed)
    time.sleep(0.5)

def forward():
    PressKey(0x11)
    ReleaseKey(left_pressed)
    ReleaseKey(right_pressed)
    time.sleep(0.5)

mp_drawing = mp.solutions.drawing_utils #helps to render the landmarks
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
# You can setup your camera settings
# cap.set(3,1920)
# cap.set(4,1080)


with mp_hands.Hands(min_detection_confidence=0.5 , min_tracking_confidence=0.5,max_num_hands=1) as hands:


    while cap.isOpened():

        re, frame = cap.read()

        # start the detection
        # ===================

        # convert the image to RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        # flip the image
        image = cv2.flip(image,1)

        image.flags.writeable = False

        # this is the main process
        results = hands.process(image)

        image.flags.writeable = True

        # print the results
        #print(results.multi_hand_landmarks)
        image_height, image_width, _ = image.shape
        image = cv2.line(image,(213,0),(213,500),(255,255,0),3)
        image = cv2.line(image,(426,0),(426,500),(255,255,0),3)
        
        cv2.putText(image,'LEFT',(10,300),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
        cv2.putText(image,'RIGHT',(440,300),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
        cv2.putText(image,'N',(320,300),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)

        if results.multi_hand_landmarks:
            
 
            #for num, hand in enumerate(results.multi_hand_landmarks):
            #    mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS)

            # lets change the colors and the dots and joits
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255,0,0),thickness=2 , circle_radius=4),
                mp_drawing.DrawingSpec(color=(0,255,255),thickness=2 , circle_radius=2))

                # print(
                #         f'Index finger tip coordinates: (',
                #         f'{hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                #         f'{hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                # )

                x1=hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
                y1=hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                title = gw.getActiveWindow().title
                if title=='Need for Speed™ Most Wanted' or 'Ultrawide' or 'Offroad Racers':
                    if x1<=213:
                        left()
                    elif x1>=440:
                        right()
                    else:
                        forward()
                

        # recolor back the image to BGR
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('image',image)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break



cap.release()
cv2.destroyAllWindows()