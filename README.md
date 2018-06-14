# RioCV-PI
opencv for the roborio using a raspberry pi and networktables

## Installation
To install all python libraries with pip, use
```
pip install scipy numpy imutils opencv-python-headless pynetworktables
```
Then install php7 using your prefered method

## Running
First, start the frame server `php -S 0.0.0.0:2081` Then, start the script `python3 vision.py -c 99`
