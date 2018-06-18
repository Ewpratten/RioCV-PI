# A modified facial recognition script for detecting powercubes
import cv2
import os
import numpy as np
import urllib.request

def assure_path_exists(path):
    dir = os.path.dirname(path)
    print("Setting file path...")
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Creating folder...")


# For each person, one face id
face_id = 1

# Initialize sample face image
count = 0

assure_path_exists("./dataset/")

def convert(frame):
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) # blur
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # convert colors
    return hsv

# Start looping
while(True):

    # Capture video frame
    with urllib.request.urlopen("http://localhost:2015/getframe.php") as url:
        imgReard = url.read()
    imgNp = np.array(bytearray(imgReard), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    img = cv2.resize(img, (900, 540))
    image_frame = img

    # Convert frame to grayscale
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
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

    # Loops for each faces
    if len(cnts) > 0:
    	# Find center of cube and radius
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # Decide weather to send a speed or 0 depending on confidence
        if radius > accuracy:

	        # Crop the image frame into rectangle
	        cv2.rectangle(frame, (x - radius, y - radius), (x + radius, y + radius), (255,0,0), 2)
	
	        # Increment sample face image
	        count += 1
	
	        # Save the captured image into the datasets folder
	        cv2.imwrite("./dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
        # cv2.imshow('frame', image_frame)
    print("Count: " + str(count))
    # To stop taking video, press 'q' for at least 100ms
    # if cv2.waitKey(100) & 0xFF == ord('q'):
    #     break

    # If image taken reach 100, stop taking video

    elif count>100:
        break

# Stop video


# Close all started windows
cv2.destroyAllWindows()
