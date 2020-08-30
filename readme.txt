I can't get ctypes to work on Windows cus Windows is just the worst

To get it to work on Windows, you'll have to figure out how to compile the C code into
a .dll file, which is harder than it sounds. The most common method that I was able to find
was to use Microsoft Visual Studio (not VS Code) to do it for you. I couldn't for the life of
me figure out how to do it with gcc.


All this code WILL work on Linux however.

If you have a hard time installing pyaudio, you might need to run the following commands,
then try again:

	sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
	sudo apt-get install ffmpeg libav-tools
	sudo pip3 install pyaudio

