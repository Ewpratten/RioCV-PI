# import threading
# import os

# exitFlag = 0

# class threader (threading.Thread):
#   def __init__(self, threadID, name, command):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.command = command
#   def run(self):
#       print ("Starting " + self.name)
#       os.system(self.command)
#       print ("Exiting " + self.name)

# print("Reminder that this script requires Php7.2 installed along with all of the python libs listed in README.md file")

# if arg1 == "start":
# 	thread1 = threader(1, "WebServer", "php -t ./WebServer/ -S 0.0.0.0:2015")
# 	thread2 = threader(2, "VisionServer", "python3 ./Scripts/vision.py -c 99")

print("This script is currently disabled. Please run the following commands in seprate terminals")
print("php -t ./WebServer/ -S 0.0.0.0:2015")
print("python3 ./Scripts/vision.py -c 99")