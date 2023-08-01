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

WAIT_TIME = 0.5 # MARK: Tweak to increase delay on detections
TWISTS_PER_ID = {0:1, 1:2, 15:3}
KNOWN_MARKERS = set(TWISTS_PER_ID.keys())

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# profile = pipeline.start(config)
print("camera started")

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters()
refine_param = cv2.aruco.RefineParameters()
# parameters.aprilTagMinClusterPixels = 1
# parameters.aprilTagCriticalRad = 0

detector = cv2.aruco.ArucoDetector(aruco_dict, parameters, refine_param)

def call_camera(car: NvidiaRacecar):
    profile = pipeline.start(config)

    frames = pipeline.wait_for_frames() # REVIEW: check this
    frame = frames[0]
    color_image = np.asanyarray(frame.get_data())
    color_image = color_image[...,::-1].copy()

    accepted, ids, rejected = detector.detectMarkers(color_image)
    if ids is not None and len(ids) > 0:
        # TODO ignore repeat ArUco ids
        # Range: ~12 m
        print(ids)
        try:
            for id in ids:
                if id[0] in KNOWN_MARKERS:
                    print("Stop the main thread")

                    print("Spotted # ", id)
                    car.throttle = 0.0
                    for _ in range(TWISTS_PER_ID[id[0]]): # twist n times
                        car.steering = 0.5
                        time.sleep(WAIT_TIME)
                        car.steering = -0.5
                        time.sleep(WAIT_TIME / 2)
        except Exception as e:
            print("Failed:", e)

    pipeline.stop()
    print("stopped")


if __name__ == '__main__':
    print("hello world i am camera")
