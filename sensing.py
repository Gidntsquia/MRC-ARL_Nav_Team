import threading
import time

import pyrealsense2 as rs

__author__ = "Addison Hanrattie", "Jaxon Lee"
__copyright__ = "Copyright 2023, Maryland Robotics Center"
__credits__ = ["Addison Hanrattie", "Nicky Sremac-Saari", "Jordan White"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jaxon Lee"
__email__ = "jaxondlee@gmail.com"
__status__ = "Development"

pipeline = rs.pipeline()
config = rs.config()

def sensing_thread(event : threading.Event):
    """Thread for detecing ArUco markers and acting on that information.

    Args:
        event (threading.Event): Event that stops the spiraling code. 
            Run 
    """
    print("Hello")
    while True:
        time.sleep(3)
        event.clear()
        print("STOP Main thread prints")
        time.sleep(5)
        event.set()


if __name__ == '__main__':
    print("hello world")