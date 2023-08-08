# MRC-ARL Nav Team :robot:
Robot code for the MRC-ARL summer internship at the University of Maryland for Summer 2023.

![MRC-ARL_Robot](https://github.com/Gidntsquia/MRC-ARL_Nav_Team/assets/32310846/a2710ece-6c81-4e85-815c-19a446631668)

See more details about the program here:
[Flyer](https://bpb-us-e1.wpmucdn.com/blog.umd.edu/dist/d/961/files/2023/03/ARLSummerResearchExperienceFlyer2023.pdf)

## Quickstart :rocket:
```
git clone https://github.com/Gidntsquia/MRC-ARL_Nav_Team
python3 setup.py  # This installs required packages.
python3 main.py
```

IMPORTANT: Make sure to turn the motors on before starting! There is a switch on the back
middle right of the robot. A small red light near the switch will turn red and 
it will beep when the motors are on.

The robot takes a few seconds to load up, then it will be controllable
with a remote controller! Note: the motors won't run until the robot 
is told to go forward a few times due to the internal motor controller.

Team members: Addison Hanrattie, Jaxon Lee, Nicky Sremac-Saari, and Jordan White

## Detailed Setup 🧑‍🔬
Firstly, if we want to get the code onto the Jetson Nano and run it there, we need a way to connect to it. Here are two methods:


### Monitor Method 🖱️
1. Ensure the Jetson Nano's power supply is charged. Turn it on.
2. Connect a keyboard, monitor, and mouse to the Jetson Nano. The Ubuntu OS
should show up on the screen.
3. Navigate to the "terminal" application.
4. We are now connected to the Jetson Nano!

  
### Laptop Method 💻
1. Ensure the Jetson Nano's power supply is charged. Turn it on.
2. Connect your laptop to the same wifi that the Jetson Nano is connected to.
    The Jetson Nano will automatically connect to whatever WiFi it was last 
    connected to. If it doesn't connect to any WiFi, use the MONITOR METHOD to
    bring up the Ubuntu OS, and you can simply connect to WiFI from there just
    like you would with a Windows/Mac machine. Also, make sure to turn on
    "automatic login" since otherwise the Jetson will not be accessible until
    you enter the password (which can only be done with the MONITOR METHOD).
3. With that done, run the following code:

        ssh jetson@IP_ADDRESS_HERE  (note: IP address on robot's screen)
        # Say yes to SSH'ing into the Jetson Nano
4. We are now connected to the Jetson Nano!

------
Now, we must download the repository to the Jetson Nano and install all the required pacakges. Run the following code in the terminal we opened in the previous step:

```
cd
git clone https://github.com/Gidntsquia/MRC-ARL_Nav_Team
python3 ~/MRC-ARL_Nav_Team/setup.py
pip install numpy
```

TODO: Add installation instructions for these python libraries: cv2 and pyrealsense2

After this, we can run the code:

```
python3 ~/MRC-ARL_Nav_Team/main.py
```

If there is an issue relating to "gpiochip" file not existing, run this to fix it:
```
sudo usermod -aG gpio $USER
sudo chown root.gpio /dev/gpiochip0
sudo chmod 660 /dev/gpiochip0
```

To control the robot with the remote controller, ensure the 
Bluetooth receiver is plugged into the Jetson Nano, the remote controller is on, the 
"home" button is pressed. The robot can be controlled with the remote controller as
follows:
```
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
```

