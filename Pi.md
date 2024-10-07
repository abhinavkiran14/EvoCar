# Pi
This documentation covers things on the pi. 

The pi has several custom systemd services:

`evocar.service`: the webserver that hosts the web ui

It has several valuable api's

Using `/command?cmd=[shutdown|reboot]` you can shutdown or reboot this is a GET request

Using `/command?cmd=direct&v1=[encoded json for motor speeds/positions]` this is a GET request

Using `/getpositions` return the saved waypoints for each program

Using `/getkits` return the names and data of custom kits of the arm

Using `/getpos` returns the current servo angles and motor speeds only if the arduino is plugged in

Using `/getstatus` returns the current servo angles and motor speeds and other misc. data only if the arduino is plugged in

Using`command?cmd=service[start|stop|restart]&v1=camera` you can restart the camera service. As far as I can tell this only works with the camera service

Using `/camconfig` you use &name=[framerate|port|resolution]&value=[<anything>]&type=[int|string]
`evoduino.service`: the service that interacts with the arduino I think

`shutdownbutton.service`: A service ready to shutdown for the shutdown button I believe. I do not know why this is not just a function of evocar

`camera.service`: Hosts the camera feed (usually port 8000). 

/ and /index.html gives it as html and is choppy. 
/frame.jpg gives the frame at the time of the request and nothing else. 
/stream.mjpg gives a live updating stream and is what we want to use

Camera uses a file called `camconfig.json` for how to read the video. 

`rosmasterpi.service`: This starts ros and hosts its master node I believe.

`getmyip.service`: Gets ip???



