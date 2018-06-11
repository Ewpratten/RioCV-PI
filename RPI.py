######## Start Notes ########
# To install all libraries, run:
# pip install scipy numpy imutils opencv-python-headless pynetworktables

# The URL for Mjpg streams off the RoboRIO is:
# http://10.TE.AM.2:1181/stream.mjpg
######## End Notes ########

# Import Required Libraries
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time
import urllib.request
from scipy.interpolate import interp1d
from networktables import NetworkTables
import logging


######## Start Configuration ########
is_logging =  True         # Setting to False will speed up program
ip_address = "10.50.24.2"  # Default IP address of RoboRIO
camera_id  =  0            # Default camera id
speed      =  0.535        # How fast should the robot move forward? (ranges from -1.0 to +1.0)
accuracy   =  10           # How confident should the robot be before locking on to an object? (ranges from 0 to camera height)
deadzone   =  5            # Deadzone around center of camera in pixels
max_range  =  0.8          # Max speed
min_range  = -0.8          # Min speed
######## End Configuration ########

# HSL bounds of "Green" (actually yellow)
greenLower = (29, 86, 6)    # Lower bound
greenUpper = (64, 255, 255) # Upper bound

# Set arguments and create help info
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip",     type=str, default=ip_address, help="Ip address of networktables server")
ap.add_argument("-b", "--buffer", type=int, default=64,         help="max buffer size")
ap.add_argument("-c", "--camera", type=int, default=camera_id,  help="Camera Port")
args = vars(ap.parse_args())

# Create the Mjpg server URL from data above
server  = "http://"
server += args["ip"]
server += "/stream.mjpg"

# Enable logging to stdout & Initialize NetworkTables
logging.basicConfig(level=logging.DEBUG)      # Set logging mode
NetworkTables.initialize(server=args["ip"])   # Init NT with RoboRIO IP address
NetworkTables.initialize()                    # Finish NT init
sd = NetworkTables.getTable("SmartDashboard") # Get SmartDashboard table

# Set max buffer size based on argument
pts = deque(maxlen=args["buffer"])

# If NOT using Mjpg stream, Init camera
if(args["camera"] != 99):
    vs = VideoStream(src=args["camera"]).start() # Init camera

# Create Maps
pixel_map    = interp1d([0, 600], [min_range, max_range])      # Map pixel value to motor speed
deadzone_map = range((300 - deadzone +1), (300 + deadzone +1)) # Handle deadzones

######## Start Functions ########
def LOG(x):
	if is_logging:
		print(x)

def convert(frame):
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) # blur
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # convert colors
    return hsv

def sendData(x,y):
    if(y == 0 or y == 2):
        s = float("{0:.2f}".format(float(pixel_map(x))))
    else:
        s = 0.0
    if s in deadzone_map:
        z = 0.0
    else:
        z = s
    sd.putNumber('camx', (z * 100 ))
    sd.putNumber('fspeed', (speed * 100))
    LOG(z)

######## End Functions ########


time.sleep(2.0) # Pause for camera to start up
while True: # Main loop
    
    if(args["camera"] == 99):
        with urllib.request.urlopen(server) as url:
            frame = url.read()
        frame = np.array(bytearray(frame), dtype=np.uint8)
        frame = cv2.imdecode(frame, -1)

    else:
        frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # If frame not found, the video has stopped
    if frame is None:
        break
    
    # Resize frame
    frame = imutils.resize(frame, width=600)
    
    # Get HSV varsion of frame
    hsv = convert(frame)

    # Build frame mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask and initialize the current (x, y) center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # Only proceed if at least one contour was found
    if len(cnts) > 0:
    	# Find center of cube and radius
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # Decide weather to send a speed or 0 depending on confidence
        if radius > accuracy:
            sendData(int(x), 0) # Send calculated speed
        else:
            sendData(0,1) # Send 0.0

    # Update the points queue
    pts.appendleft(center)

if not args.get("video", False):
    vs.stop()

else:
    vs.release()
# On some computers, the following line is needed
#cv2.destroyAllWindows()
