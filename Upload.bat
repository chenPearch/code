@echo off
title uploder
rem this file uploads the
rem Main.py and opencvBasic.py files
rem on to the raspberry pi
echo uploding 

SET _CWD=C:\Users\chen7\Documents\FRC\visionprossing\code
SET _PI_IP=10.45.86.69
SET _TARGET_FOLDER=/home/pi/frcvision

pscp -pw root %_CWD%\helperFile.py pi@%_PI_IP%:%_TARGET_FOLDER%
pscp -pw root %_CWD%\Main.py pi@%_PI_IP%:%_TARGET_FOLDER%
pscp -pw root %_CWD%\ HSVdata.json pi@%_PI_IP%:%_TARGET_FOLDER%
echo finished uploading
