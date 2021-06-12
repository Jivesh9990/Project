import numpy as np
import cv2

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX


while True:
    ret, frame = cap.read()
    frame = cv2.line(frame,(200,0),(200,500),(255,255,0),3)
    frame = cv2.line(frame,(400,0),(400,500),(255,255,0),3)
    frame = cv2.line(frame,(200,160),(400,160),(255,255,0),3)
    frame = cv2.line(frame,(200,325),(400,325),(255,255,0),3)
    cv2.putText(frame,'Left',(75,270), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'forward',(240,80), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'Neutral',(240,260), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'Backward',(230,420), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,'Right',(480,270), font, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()