# open-cv vision solution for RPI3
**vision solution** is simple solution to a big problem in FRC image proccesing.
the main problem that this project solves is deploying the python code to the [Raspberry Pi](https://www.raspberrypi.org/)

## how to use this project
using this project is pretty simple. 

first of all you need to have [Putty](https://www.putty.org/) to use pscp to upload the files.

and change the environment veriables written in the Upload.bat file.
e.g.
```
SET _CWD=<your current working directory>
SET _PI_IP=<your raspberry pi's ip>
SET _TARGET_FOLDER=<the targes folder in the pi's ip>
```
when you finished writing your code just type ```Upload.bat``` in to the command line and you are done.

