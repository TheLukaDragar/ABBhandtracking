#CONFIG FILE
#Made by Luka Dragar
#@thelukadragar
operatingmode="xyz"
#"xy"---move only in xy
#"xyz"--move in xy and z
#----------------------------------------------
sendinginterval=0.15
#interval to send points[seconds] 
#try changing if there are problems
myIP="192.168.64.101"
myPort=55555

#limit coordinates for moving 
#change if robot out of reach
xmax=600 
xmin=0

ymin=0
ymax=600

zmax=300
zmin=-500
zrange=1000 #difference betwen max and  min 

zoffsetcamera=-500#offset according to where you want Z0 to be 
areatocompare=120000#compares area of your hand to this value


#scale in percent
livefeedwindowscalex=100
livefeedwindowscaley=100

#coordinatemultiplier
cormultiplyx=1
cormultiplyy=1
cormultiplyz=1

#sensitivity send move if object moves by px +-1 default
sensitivity=1
