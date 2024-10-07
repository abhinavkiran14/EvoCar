# Code 

This file describes the directory structure and what each not self explanatory file does. An example of a not self explanatory file would be \_\_init\_\_.py

### main.py
This contains the main loop and main function and "glues" together all the parts of the program.

### evocar.py
This contains the evocar class which provides abstractions for interacting with the pi. It can control motors and servos as well as turn the camera on or off.


### load\_settings.py
This file is used to load default.json and settings.json. First, it attempts to load default.json and then if available it loads the filename passed into it.

### img\_proc.py
This contains the functions used to process the image and find the lines etc. This is essentially described in `Method.md`

### line.py
This contains the classes `Line` and `Rectangle` for `img_proc.py` for processing images.

### Makefile
This is a makefile to provide convenient ways to run and test the program.

`make` or `make run`: runs `main.py`

`make test`: runs the unittests for all of the python files

`make benchmark` or `make bench`: runs bench.py to run the benchmark

### videoget.py
This file gets the video in another thread allowing you to fetch the latest frame instantly from another thread.

### settings.json
Contains key value pairs for the ip, ports, PID values, arm positions, and other configurations.

### default.json
Same as settings.json but is the defaults that have close but not quite good values.
