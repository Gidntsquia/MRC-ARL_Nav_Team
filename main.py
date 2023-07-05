#!/usr/bin/env python3
"""Autonomous navigation code for MRC-ARL internship robot project.
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

def main():
    print("Hello World!")
    car = NvidiaRacecar()
    print("Set up!")
    
    car.steering = 1
    time.sleep(1)
    print(car.throttle_gain)
    car.throttle = 0.15
    
    
    start_time = time.time()
    
    while (car.steering > 0.0 and time.time() - start_time < 20):
        car.steering -= 0.005
        time.sleep(0.5)
    
    print("Done")
    car.throttle = 0.0
    
    print("Goodbye World... :(")
    
    
    
if __name__ == '__main__':
    main()