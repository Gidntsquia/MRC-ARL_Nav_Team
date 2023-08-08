#!/usr/bin/env python3
"""Autonomous navigation code for MRC-ARL internship robot project.
To control the robot with the remote controller:
1.  Ensure you have the Jetracer with Jetson Nano on it, the remote controller,
    and the Bluetooth USB receiver.
2.  Turn on the Jetson Nano. Connect to the Jetson Nano with one of these methods:
    MONITOR METHOD
    Connect a keyboard, monitor, and mouse to the Jetson Nano. The Ubuntu OS
    should show up on the screen. Navigate to the "terminal" application and run
    the following code:
        `python3 ~/MRC-ARL_Nav_Team/main.py`
    
    LAPTOP METHOD
    Connect your laptop to the same wifi that the Jetson Nano is connected to.
    The Jetson Nano will automatically connect to whatever WiFi it was last 
    connected to. If it doesn't connect to any WiFi, use the MONITOR METHOD to
    bring up the Ubuntu OS, and you can simply connect to WiFI from there just
    like you would with a Windows/Mac machine. Also, make sure to turn on
    "automatic login" since otherwise the Jetson will not be accessible until
    you enter the password (which can only be done with the MONITOR METHOD).
    With that done, run the following code:
        `ssh jetson@IP_ADDRESS_HERE  (note: IP address on robot's screen)
        # Say yes to SSH'ing into the Jetson Nano
        # You should now be connected to the Jetson Nano through SSH
        python3 ~/MRC-ARL_Nav_Team/main.py`
    
3. Connect Bluetooth USB receiver to Jetson Nano on robot 
4. Turn on the remote controller and press the "home" button
5. The robot should be controllable with the following interface:
    Left joystick vertical axis     : throttle speed forward/back
    Left joystick horizontal axis   : steering left/right
    "home"                          : connect controller to the robot
    "Y"                             : increase max speed
    "A"                             : decrease max speed
    "X"                             : take picture with camera and do dance if
                                      ArUco marker is detected. NOTE: will stop
                                      robot control until the picture taking
                                      process is finished.
    All other buttons don't do anything.

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
import time 
from nvidia_racecar import NvidiaRacecar

from sensing import call_camera
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
    car.throttle = 0.0
    time.sleep(0.5)

    # This should turn the motor encoder on
    return car



def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def do_remote_control(car: NvidiaRacecar):
    car.steering_offset = -0.2
    car.throttle_gain = -0.2
    controller = RemoteController()
    controller.init()
    print("Remote Set up!")
    time.sleep(1)

    try:
        while True:
            controller_inputs = controller.listen()
            car.throttle_gain = controller.my_throttle_gain
            throttle_input = controller_inputs[1][1]
            car.throttle = throttle_input
            steering_input : float = controller_inputs[1][0]
            # temp = steering_input
            steering_input = clamp(steering_input, -0.8, 1.0)
            # print(temp, "->", steering_input)
            car.steering = steering_input

            if controller_inputs[0][3]:
                call_camera(car)

    except KeyboardInterrupt:
        print("interrupted")


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
        # do_spiral_method(car)
        do_remote_control(car)
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
