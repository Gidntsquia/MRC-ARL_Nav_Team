#!/usr/bin/env python3
"""
"""

__author__ = "Addison Hanrattie", "Jaxon Lee"
__copyright__ = "Copyright 2023, Maryland Robotics Center"
__credits__ = ["Addison Hanrattie", "Nicky Sremac-Saari", "Jordan White"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jaxon Lee"
__email__ = "jaxondlee@gmail.com"
__status__ = "Development"


from nvidia_racecar import NvidiaRacecar
import threading
import time

import numpy as np

import cv2
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
profile = pipeline.start(config)

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
# parameters.aprilTagMinClusterPixels = 1
# parameters.aprilTagCriticalRad = 0

def sensing_thread(car : NvidiaRacecar, event : threading.Event):
    """Thread for detecting ArUco markers and acting on that information.

    Args:
        event (threading.Event): Event that stops the spiraling code. 
            Run event.clear() to stop the main thread
            Run event.set() continues the thread again
    """
    print("Hello")
    while True:
        frames = pipeline.wait_for_frames() # REVIEW: check this
        frame = frames[0]
        color_image = np.asanyarray(frame.get_data())
        color_image = color_image[...,::-1].copy()
        
        accepted, ids, rejected = cv2.aruco.detectMarkers(color_image, aruco_dict, parameters=parameters)
        print("Detecting")
        if ids != None and len(ids) > 0:
            # TODO ignore repeat ArUco ids
            # Range: ~12 m
            print(ids)
            event.clear()
            print("Stop the main thread")
            car.steering = 0.33
            time.sleep(0.5)
            car.steering = -0.33
            time.sleep(0.5)
            print("Release!")
            event.set()


if __name__ == '__main__':
    print("hello world")