#!/usr/bin/env python3
"""Autonomous navigation code for MRC-ARL internship robot project.

Guide to interfacing with robot-
    car = NvidiaRacecar()  : initializes car, you can control it w/ "car" object 
    car.throttle = [-1.0, -0.15] U [0.15, 1.0]      : sets motor speed
    car.steering = [-1.0, 0.0) U (0.0, 1.0]         : sets motor steering    
     
    actual_throttle = car.throttle_gain * car.throttle
    actual steering = car.steering_gain * car.steering + car.steering_offset
    
    
Known issues:
    - Steering radius is [-0.15, 0.15]
    - Robot has high-pitched humming noise when it drives
    - Sometimes robot stops and can't drive itself forwarad unless pushed
"""
from nvidia_racecar import NvidiaRacecar
import time

__author__ = "Jaxon Lee"
__copyright__ = "Copyright 2023, Maryland Robotics Center"
__credits__ = ["Addison Hanrattie", "Nicky Sremac-Saari", "Jordan White"]
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jaxon Lee"
__email__ = "jaxondlee@gmail.com"
__status__ = "Development"


def setup(car : NvidiaRacecar):
    """Force motor encoders to turn on and set steering to initial position.
    """
    car.steering_offset = -0.2
    #car.throttle = 0.2
    #time.sleep(0.5)
    car.throttle = 0.0
    time.sleep(0.5)
    
    # This should turn the motor encoder on
    return car
    
    
def do_spiral_method(car : NvidiaRacecar):    
    """Apply the spiral method for traversing ARL location.

    Args:
        car (NvidiaRacecar): robot object
    """
    car.steering = -0.15
    time.sleep(1)
    print(car.throttle_gain)
    car.throttle = 0.175
    while (True):
        pass
    
    start_time = time.time()
    
    while (car.steering < 0.0 and time.time() - start_time < 30):
        car.steering += 0.005
        time.sleep(0.5)
    
    if (time.time() - start_time >= 30):
        print("Timeout reached.")
    

def main():
    """Area for main program. This method is called when calling this file
    in the terminal.
    """
    # Initial setup
    print("Hello World!")
    car = NvidiaRacecar()  # Takes a few seconds
    setup(car)
    print("Set up!")
    
    
    # Main code
    ## Do this so that car throttle is set to 0 at the end.
    try:
        do_spiral_method(car)
    except KeyboardInterrupt:
        pass
    
    
    
    # Closing things
    print("Done")
    car.steering = 0.0001
    car.throttle = 0.0
    print("Goodbye World... Until next time!")
    
    time.sleep(1.0)
    
    
    
if __name__ == '__main__':
    main()