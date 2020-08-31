__doc__ = """A thread to stream audio from your computer's microhpone"""
__author__ = "Ryan Mah"

import threading
import time
import queue
import pyaudio
import numpy as np


class Audio_Streamer(threading.Thread):
	def __init__(self, out_queue):
		"""out_queue should be an instance of queue.Queue"""
		threading.Thread.__init__(self)
		self.daemon = True

		self.FORMAT = pyaudio.paInt16 	# use 16-bit bit depth
		self.CHANNELS = 1
		self.SAMPLE_RATE = int(44.1E3)
		self.BINS = 1 << 15

		self.GRACE_PERIOD = 0			# time period to allow signal processing algorithms to run.
										# I think pyaudio is actually too slow for me to need this, 
										# but I'll leave it in just in case 

		self.buffer = out_queue
		self._running = True

		self.audio = None
		self.stream = None


	def run(self):
		"""Overriding threading.Thread run method"""
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(
		    format = self.FORMAT,
		    channels = self.CHANNELS,
		    rate = self.SAMPLE_RATE,
		    input = True
		)
		self.stream.start_stream()
		while True:			
			if not(self._running):
				break		

			samples = np.frombuffer(self.stream.read(self.BINS), np.int16)
			self.buffer.put(samples)

			start = time.time()
			while (time.time() - start) < self.GRACE_PERIOD:  # wait for grace period to complete
				time.sleep(0.000000001)

	def stop(self):
		self._running = False

		self.stream.stop_stream()
		self.stream.close()
		self.audio.terminate()

		self.audio = None
		self.stream = None

	def get(self):
		ret = self.buffer.get()
		return ret

		




def test_audio_streamer():
	import os
	import sys
	import matplotlib.pyplot as plt

	DIRECTORY = os.path.dirname(os.path.abspath(__file__))
	SRC_DIR = os.path.dirname(DIRECTORY)
	sys.path.append(os.path.join(SRC_DIR, "Signal-Processing", "lib"))

	import signal_processing_lib as sp


	streamer = Audio_Streamer()
	streamer.GRACE_PERIOD = 0.01
	streamer.start()
	while True:
		try:
			samples = streamer.get()
			samples = sp.adc_to_V(samples, Vref = 1, bit_depth = 16)

			freqs = sp.bins_to_freq(sample_rate = streamer.SAMPLE_RATE, N = streamer.BINS)
			
			X = sp.fft(samples)
			X = sp.high_pass_filter(X, bin_cutoff = 35)

			X = sp.harmonic_product_spectrum(freqs, X)

			# plt.plot(freqs, X)
			# plt.show()

			fundamental_freq = freqs[X.index(max(X))]
			print(f"Buffer empty = {streamer.buffer.empty()}")
			print(f"Fundamental Frequency = {fundamental_freq} Hz")
		except KeyboardInterrupt:
			break

	streamer.stop()



if __name__ == "__main__":
	test_audio_streamer()



	