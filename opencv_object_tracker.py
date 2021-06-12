# import the necessary packages
import argparse
import time
import cv2
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

video=None
tracker_choice='csrt'
OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        # "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        # "tld": cv2.TrackerTLD_create,
        # "medianflow": cv2.TrackerMedianFlow_create,
        # "mosse": cv2.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS[tracker_choice]()

initBB = None


if not video:
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(0)
    time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(video)
    height, width = (
    int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    int(vs.get(cv2.CAP_PROP_FRAME_WIDTH)),)
    fps = vs.get(cv2.CAP_PROP_FPS)
    print(height,width)
# initialize the FPS throughput estimator




while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    try:
        title = gw.getActiveWindow().title
    except:
        
        title=''
    state,frame = vs.read()
    # check to see if we have reached the end of the stream
    frame = cv2.line(frame,(320,0),(320,500),(255,255,0),3)
    
    
    if frame is None:
        break
    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
    image = cv2.flip(frame, 3)
    (H, W) = frame.shape[:2]


    
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
            x2=x+w
            y2=y+h
            print(title)
            print(x2,y2)
            if title=='Need for Speed™ Most Wanted':
                if x2<=210:
                    left()
                    print('LEFT')
                    cv2.putText(frame,'LEFT',(10,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
                elif x>=280:
                    right()
                    print('RIGHT')
                    cv2.putText(frame,'RIGHT',(400,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
                else:
                    cv2.putText(frame,'N',(100,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
                    forward()
            


        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", tracker_choice),
            ("Success", "Yes" if success else "No"),
            ("coords",f"{x,y,w,h}")
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



    cv2.imshow("image", frame)
    key = cv2.waitKey(1)
    # if the 's' key is selected, we are going to "select" a bounding
    # box to track

    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("image", frame, fromCenter=False,showCrosshair=True)
        cv2.destroyWindow("image")

        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
      
        print('Tracker Created')



    elif key == ord("q"):
        break
# if we are using a webcam, release the pointer
if not video:
    vs.stop()
# otherwise, release the file pointer
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
