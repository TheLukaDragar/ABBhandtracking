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
Launch Tracking python ForcePowers_start.py
It should connect and print the Robot position in terminal
Wait for camera to start 
Position your object in the green squares so it can capture its color then press z !
tracking will start robot will move 

change configuration(xyz,xy) by pressing c
pause by pressing p
exit with esc
recapture color by pressing z

if error occurs check terminal and press any key

edit config.py if necessary.

# Tips
have good lighting
use object with a unique color 
have all windows open 

# Troubleshooting
if u want to use commands u have to click the Camera live feed window
for any questions write to me at lukadragarbusiness@gmail.com I will be happy to help



