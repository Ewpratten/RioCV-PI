from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import numpy as np
import time
import urllib.request
from scipy.interpolate import interp1d
from networktables import NetworkTables
import logging

ip = "10.50.24.2"
def valueChanged(table, key, value, isNew):
	print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

def connectionListener(connected, info):
	print(info, '; Connected=%s' % connected)

# logging.basicConfig(level=logging.DEBUG)      # Set logging mode
NetworkTables.initialize(ip)   # Init NT with RoboRIO IP address
NetworkTables.initialize()
# binascii.unhexlify(error)
sd = NetworkTables.getTable("DriverStation")
sd.addEntryListener(valueChanged)

while True:
    time.sleep(1)