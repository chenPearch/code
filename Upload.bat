@echo off
title uploder
rem this file uploads the
rem Main.py and opencvBasic.py files
rem on to the raspberry pi
echo uploding 
pscp -pw root C:\Users\chen7\Documents\FRC\visionprossing\code\helperFile.py pi@10.45.86.69:/home/pi/frcvision
pscp -pw root C:\Users\chen7\Documents\FRC\visionprossing\code\Main.py pi@10.45.86.69:/home/pi/frcvision
pscp -pw root C:\Users\chen7\Documents\FRC\visionprossing\code\HSVdata.json pi@10.45.86.69:/home/pi/frcvision
