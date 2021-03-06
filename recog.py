#------------------------------------------------------------
# SEGMENT, RECOGNIZE and COUNT fingers from a video sequence
#------------------------------------------------------------

# organize imports
import cv2
import imutils
import numpy as np
import time
from sklearn.metrics import pairwise
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

# global variables
bg = None

#--------------------------------------------------
# To find the running average over the background
#--------------------------------------------------
def run_avg(image, accumWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, accumWeight)

#---------------------------------------------
# To segment the region of hand in the image
#---------------------------------------------
def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

#--------------------------------------------------------------
# To count the number of fingers in the segmented hand region
#--------------------------------------------------------------
def count(thresholded, segmented):
    # find the convex hull of the segmented hand region
    chull = cv2.convexHull(segmented)

    # find the most extreme points in the convex hull
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])

    # find the center of the palm
    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)

    # find the maximum euclidean distance between the center of the palm
    # and the most extreme points of the convex hull
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]

    # calculate the radius of the circle with 80% of the max euclidean distance obtained
    radius = int(0.8 * maximum_distance)

    # find the circumference of the circle
    circumference = (2 * np.pi * radius)

    # take out the circular region of interest which has 
    # the palm and the fingers
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")

    # take bit-wise AND between thresholded hand using the circular ROI as the mask
    # which gives the cuts obtained using mask on the thresholded hand image
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    # compute the contours in the circular ROI
    ( cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # # initalize the finger count
    # count = 0

    # # loop through the contours found
    # for c in cnts:
    #     # compute the bounding box of the contour
    #     (x, y, w, h) = cv2.boundingRect(c)

    #     # increment the count of fingers only if -
    #     # 1. The contour region is not the wrist (bottom area)
    #     # 2. The number of points along the contour does not exceed
    #     #     25% of the circumference of the circular ROI
    #     if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
    #         count += 1

    return circular_roi,cX,cY

#--------------------------------------------------------------
# To send the instruction to game
#--------------------------------------------------------------

def update_controls(cx,cy):
    if cy>300:
        # cv2.putText(frame,'N',(100,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
        forward()
        if cx < 320:
            left()
            forward()
            print('LEFT')
            # cv2.putText(frame,'LEFT',(10,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
        elif cx>320:
            right()
            forward()
            print('RIGHT')
            # cv2.putText(frame,'RIGHT',(400,40),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
    
#-----------------
# MAIN FUNCTION
#-----------------

def main(camera=0,accumWeight = 0.5):
    # initialize accumulated weight
    # get the reference to the webcam
    camera = cv2.VideoCapture(camera)
    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()
        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 3)
        # get the height and width of the frame
        (height, width) = frame.shape[:2]

       

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our weighted average model gets calibrated
        if num_frames < 30:
            run_avg(gray, accumWeight)
            msg = "[STATUS] please wait! calibrating..."
            if num_frames == 29:
                msg = "[STATUS] calibration successfull..."
            cv2.putText(frame, msg, (15,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # # draw the segmented region and display the frame
                # cv2.drawContours(frame, segmented, -1, (0, 0, 255))

                # count the number of fingers
                circle_roi,cx,cy = count(thresholded, segmented)

                # draw the circular ROI
                cv2.circle(frame, (cx, cy), 1, (255,0,0), 6)
                cv2.circle(circle_roi, (cx, cy), 1, (255,0,0), 6)
                cv2.putText(frame, "controller", (cx - 25, cy - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,0),2)
                cv2.line(frame,(0,300),(width,300),(0,0,255),3)
                cv2.line(frame,(320,300),(320,height),(0,0,255),3)
                # show the thresholded image

                # cv2.imshow("Thesholded", thresholded)
                update_controls(cx,cy)
        

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", frame)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

    # free up memory
    camera.release()
    cv2.destroyAllWindows()

#-----------------
# Execution 
#-----------------


if __name__ == "__main__":
    main()