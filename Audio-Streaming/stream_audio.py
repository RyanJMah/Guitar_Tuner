import numpy as np
import pyaudio

FORMAT = pyaudio.paInt16 	# We use 16-bit format per sample
CHANNELS = 1
RATE = 44.1E3
CHUNK = 1 << 15				# (1 << 15)-bytes of data red from a buffer
RECORD_SECONDS = 0.75
WAVE_OUTPUT_FILENAME = "test.wav"

def get_audio_samples():
	audio = pyaudio.PyAudio()

	# start Recording
	stream = audio.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True
	)



	