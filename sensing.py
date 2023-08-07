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

# MARK: Disable depth steam if needed
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30) # TODO: switch to rgb

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
    frame = frames[1]
    color_image = np.asanyarray(frame.get_data())
    color_image = color_image[...,::-1].copy()

    depth_frame = frames[0].as_depth_frame()
    print("Depth in middle of screen is ", depth_frame.get_distance(depth_frame.width // 2, depth_frame.height // 2))

    print(np.amin(depth_frame.get_data()[depth_frame.get_data() > 0]))
    accepted, ids, rejected = detector.detectMarkers(color_image)
    if ids is not None and len(ids) > 0:
        # Range: ~12 m
        print(ids)
        try:
            for i in len(ids):
                id_num = ids[i][0]
                coords = accepted[i]
                if id_num in KNOWN_MARKERS:
                    print("Spotted # ", id_num)
                    print("Id is:", depth_frame.get_distance((coords[0].x + coords[2].x) // 2, (coords[0].y + coords[2].y) // 2), "away")

                    car.throttle = 0.0
                    for _ in range(TWISTS_PER_ID[id_num]): # twist n times
                        car.steering = 0.5
                        time.sleep(WAIT_TIME)
                        car.steering = -0.5
                        time.sleep(WAIT_TIME / 2)
        except Exception as e:
            print("Failed:", e)
    elif (len(depth_frame.get_data()[depth_frame.get_data() > 0]) > 0
          and np.amin(depth_frame.get_data()[depth_frame.get_data() > 0]) < 1.5): # if less than 1.1 meters to wall panic, ignore 0ed out values
        print("Warning: Close to Wall")

    pipeline.stop()
    print("stopped")


if __name__ == '__main__':
    print("hello world i am camera")
