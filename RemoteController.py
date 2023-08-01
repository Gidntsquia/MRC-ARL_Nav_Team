#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
# import pprint
import pygame
import time

class RemoteController():
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    def init(self):
        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = False
        self.button_data = False
        self.hat_data = False       

        self.my_throttle_gain = -0.2

        print('Pygame init complete')


    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0:0.0,1:0.0,2:0.0,3:-1.0,4:-1.0,5:0.0} #default

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()): # TODO: make more efficient
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value,2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
                print(event.button)
                if event.button == 4:
                    # Increase speed
                    self.my_throttle_gain -= 0.05
                    print("Up!", self.my_throttle_gain)
                elif event.button == 0:
                    # Decrease speed
                    self.my_throttle_gain += 0.05
                    print("Down!", self.my_throttle_gain)
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value

        return self.button_data, self.axis_data, self.hat_data

            # Insert your code on what you would like to happen for each event here!
            # In the current setup, I have the state simply printing out to the screen.

            #os.system('clear')
            #pprint.pprint(self.button_data)
            #pprint.pprint(self.axis_data)
            #pprint.pprint(self.hat_data)


if __name__ == "__main__":
    ps4 = RemoteController()
    ps4.init()
    while True:
        print(ps4.listen())
        time.sleep(1)
