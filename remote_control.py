#!/usr/bin/env python3
""" Program that manages remote controlling the robot.
"""
from nvidia_racecar import NvidiaRacecar
import time
from RemoteController import RemoteController
# from main import setup



__author__ = "Jaxon Lee"
__copyright__ = "Copyright 2023, Maryland Robotics Center"
__credits__ = ["Addison Hanrattie", "Nicky Sremac-Saari", "Jordan White"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jaxon Lee"
__email__ = "jaxondlee@gmail.com"
__status__ = "Development"

def main(car: NvidiaRacecar):
    controller = RemoteController()
    controller.init()
    print("Set up!")
    time.sleep(1)

    try:
        while True:
            controller_inputs = controller.listen()
            car.throttle_gain = controller.my_throttle_gain
            throttle_input = controller_inputs[1][1]
            car.throttle = throttle_input
            car.steering = controller_inputs[1][0]
    except KeyboardInterrupt:
        print("Interrupted")

    # Closing things
    print("Done")
    car.steering = 0.0001
    car.throttle = 0.0
    print("Goodbye World... Until next time!")

if __name__ == '__main__':
    print("Hi!")
    car = NvidiaRacecar()
    # setup(car)
    car.steering_offset = -0.2
    car.throttle_gain = -0.2
    
    main()
