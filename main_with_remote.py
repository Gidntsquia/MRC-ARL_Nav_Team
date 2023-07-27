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
    - More suspension on back side than front 
    
    
Note:
If you get issue relating to gpiochip file not existing, run these commands:
`
sudo usermod -aG gpio $USER
sudo chown root.gpio /dev/gpiochip0
sudo chmod 660 /dev/gpiochip0
`
And it should work.
"""
from nvidia_racecar import NvidiaRacecar
import time
import threading

from sensing import sensing_thread
from RemoteController import RemoteController

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

def do_remote_control(car: NvidiaRacecar, event: threading.Event):
    car.steering_offset = -0.2
    car.throttle_gain = -0.2
    controller = RemoteController()
    controller.init()
    print("Remote Set up!")
    time.sleep(1)

    try:
        while True:
            event.wait() # NOTE: will continue immediately if the event is set if not wait while sensing does its thing
            
            controller_inputs = controller.listen()
            car.throttle_gain = controller.my_throttle_gain
            throttle_input = controller_inputs[1][1]
            car.throttle = throttle_input
            car.steering = controller_inputs[1][0]
    except KeyboardInterrupt:
        print("interrupted")

def do_spiral_method(car : NvidiaRacecar, event : threading.Event):    
    """Apply the spiral method for traversing ARL location.

    Args:
        car (NvidiaRacecar): robot object
    """
    # car.steering = -0.15
    time.sleep(1)
    # Minimum 0.175
    # car.throttle = 0.16
    while (True):
        event.wait()
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

    # This event controls whether the motor does its spiral
    event = threading.Event()

    # This thread manages constantly checking for ArUco markers and stopping 
    # the robot spiral when one is detected.
    x = threading.Thread(target = sensing_thread, args = (car, event,), daemon = True)
    x.start()

    event.set()

    # Main code
    ## Do this so that car throttle is set to 0 at the end.
    try:
        # do_spiral_method(car, event)
        do_remote_control(car, event)
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
