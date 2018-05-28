import time
from networktables import NetworkTables
import socket
print(socket.gethostbyname(socket.gethostname()))

# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()

def valueChanged(table, key, value, isNew):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)


NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(valueChanged)

while True:
    time.sleep(1)
