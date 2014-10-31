# Photobooth.py

This is a small Python project that acts as a simple photo booth.


## What does it do?

When the application starts, a single window is opened and a preview from a camera begins streaming. When the user presses the space bar the application displays a countdown after which a picture is taken, stored and displayed for a few seconds. Then the application reverts to the preview mode. Pressing ESC shuts down the application.

The camera used can either be a webcam or a photo camera that is supported by gphoto2, including the capture_preview feature. At the moment the application defaults to a DSLR. If it can't connect it falls back to the webcam.


## Dependencies

- TkInter
- OpenCV
- gphoto2
- pillow
- piggypython (<https://github.com/alexdu/piggyphoto>)


Steps to run under Raspbian:

	sudo apt-get install python-tk idle python-pmw python-imaging python-imaging-tk gphoto2
	
	# gphoto2-updater
	wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh
	chmod +x gphoto2-updater.sh
	sudo ./gphoto2-updater.sh



## Usage

Just enter `python photobooth.py` in your favorite shell and you should be up and running. The pictures that are taken are stored in the folder from where the application was started. Filenames are just the date and time, in the form of yyyymmddhhmmss.jpg.


## Goals

I'd like to get this running on a Raspberry Pi. If that works I could connect an external button to start the countdown. I would also like to add controls for a relay switch to turn extra lighting on and off while taking a picture.


## Todo

- Start using Github's issue tracker in stead of this file?
- Test the application on Debian (I've been working on OSX)
- Test the application on an actual Raspberry Pi
- Cleanup 'Dependencies section' (this was just a guess) / write proper installation instructions


## Known issues

- When using a DSLR as camera, the `get_picture()` method stops working after a few images.

