# ABBhandtracking
control ABB robot using camera object detection and packets

# Instalation
Install python3

launch RobotStudio HandTracking.rspag

Edit RAPID if needed IP, PORT


pip install -r requirements.txt

cd ABB Robot movement control using camera object tracking and packets/

python ForcePowers_start.py

# How To Use

Start simulation in RobotStudio, after you configured IP and PORT correctly in RAPID and config.py

Launch tracking  with command python ForcePowers_start.py

It should connect and print the Robot position in terminal

Wait for camera to start 

Position your object in the green squares so it can capture its color then press z !

Tracking will start robot will move 

Change configuration(xyz,xy) by pressing c

Pause by pressing p

Exit with esc

Recapture color by pressing z

If error occurs check terminal and press any key

Edit config.py if necessary.

# Tips
Have good lighting

Use object with a unique color 

Have all windows open for a better view 

# Troubleshooting
If u want to use commands u have to click the Camera live feed window

For any questions write to me at lukadragarbusiness@gmail.com I will be happy to help



