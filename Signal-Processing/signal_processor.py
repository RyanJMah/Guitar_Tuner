__doc__ = """A class to process the signals coming from your computer's microhpone"""
__author__ = "Ryan Mah"

import os
import sys
import json
import threading
import queue
import numpy as np

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIRECTORY, "lib"))

import signal_processing_lib as sp


class Signal_Processor(threading.Thread):
	def __init__(self, in_queue, out_queue):
		threading.Thread.__init__(self)

		self.VREF = 1
		self.BIT_DEPTH = 16
		self.SAMPLE_RATE = int(44.1E3)
		self.BINS = (1 << 15)

		self.in_buffer = in_queue
		self.out_buffer = out_queue

		self._running = True


	def process_signal(self, samples):
		"""Takes in adc samples and returns the fundamental frequency of the samples"""
		samples = sp.adc_to_V(samples, Vref = self.VREF, bit_depth = self.BIT_DEPTH)

		freqs = sp.bins_to_freq(sample_rate = self.SAMPLE_RATE, N = self.BINS)
		
		X = sp.fft(samples)
		X = sp.high_pass_filter(X, bin_cutoff = 35)
		X = sp.harmonic_product_spectrum(freqs, X)

		return freqs[X.index(max(X))]

	def run(self):
		"""Overriding threading.Thread run method"""
		while True:
			if not(self._running):
				break

			samples = self.in_buffer.get()
			self.out_buffer.put(self.process_signal(samples))

	def stop(self):
		self._running = False




def test_signal_processor():
	SRC_DIR = os.path.dirname(DIRECTORY)
	sys.path.append(os.path.join(SRC_DIR, "Audio-Streaming"))

	from audio_streamer import Audio_Streamer


	audio_to_signal_queue = queue.Queue()
	signal_to_gui_queue = queue.Queue()

	audio_streamer = Audio_Streamer(audio_to_signal_queue)
	signal_processor = Signal_Processor(
		in_queue = audio_to_signal_queue,
		out_queue = signal_to_gui_queue
	)

	audio_streamer.start()
	audio_streamer.GRACE_PERIOD = 0.01
	signal_processor.start()

	while True:
		# this while loop simulates the GUI thread
		try:
			freq = signal_to_gui_queue.get()
			print(f"Fundamental Frequency = {freq} Hz")
		except queue.Empty:
			print("Something is wrong, the buffer is not empty...")
		except KeyboardInterrupt:
			break

	audio_streamer.stop()
	signal_processor.stop()



if __name__ == "__main__":
	test_signal_processor()




		