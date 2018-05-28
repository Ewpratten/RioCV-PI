# thanks to: https://www.bluetin.io/opencv/opencv-color-detection-filtering-python/

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time
from scipy.interpolate import interp1d
from networktables import NetworkTables
import logging
logging.basicConfig(level=logging.DEBUG)

accu = 10 #how much of a buffer on detect?
deadzone = 70 #deadzone on eather side of center (in pixels)
ranget = 0.4 #range on speed
rangeb = -0.4 #range on speed
# size 0-600

m = interp1d([0, 600], [rangeb, ranget])
r = range((300 - deadzone +1), (300 + deadzone +1))

ip = "172.16.10.109"

NetworkTables.initialize(server=ip)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

def sendc(x):
    sd.putNumber('camx', x)

def calcSpeed(x, notav):
    if(notav == 0):

        speed = float("{0:.2f}".format(float(m(x))))
        # print(speed)
        # print(x)
        return speed
    else:
        return 0.0

def prepSend(x):
    if x in r:
        print("0.0")
        return 0.0
    else:
        print(x)
        return x

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# HSL bounds of "Green" (actually yellow)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])


vs = VideoStream(src=0).start()

# allow the camera to warm up
time.sleep(2.0)

while True:
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)  #resize
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) # blur
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # convert colors

    # build mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current (x, y) center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        if radius > accu:
            sendc(prepSend(calcSpeed(int(x), 0)))
        else:
            sendc(prepSend(calcSpeed(0, 1)))

    # update the points queue
    pts.appendleft(center)

if not args.get("video", False):
    vs.stop()

else:
    vs.release()
cv2.destroyAllWindows()
