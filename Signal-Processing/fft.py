__doc__ =  """Python wrapper for signal processing algorithms written in C"""
__author__ = "Ryan Mah"

__all__ = ["fft", "bins_to_freq", "get_fundamental_freq"]

import os
import sys
import ctypes


DIRECTORY = os.path.dirname(os.path.abspath(__file__))


_fft = ctypes.CDLL(os.path.join(DIRECTORY, 'C_fft_linux.so'))
_fft.fft.restype = ctypes.POINTER(ctypes.c_float)
_fft.bins_to_freq.restype = ctypes.POINTER(ctypes.c_float)

_peak_detection = ctypes.CDLL(os.path.join(DIRECTORY, 'C_peak_detection_linux.so'))
_peak_detection.get_fundamental_freq.restype = ctypes.c_double

free = _fft.free_wrapper


def fft(x):
	N = len(x)

	x_arr = (ctypes.c_float*N)(*x)
	
	results = _fft.fft(x_arr, ctypes.c_uint(N))

	ret = [results[i] for i in range(N)]
	free(results)

	return ret



def bins_to_freq(sample_rate, N):
	results = _fft.bins_to_freq(
		ctypes.c_float(sample_rate),
		ctypes.c_uint(N)
	)

	ret = [results[i] for i in range(N)]
	free(results)

	return ret



def get_fundamental_freq(x, freqs, threshold):
	assert(len(x) == len(freqs))
	N = len(x)

	x_arr = (ctypes.c_float*N)(*x)
	freq_arr = (ctypes.c_float*N)(*freqs)

	result = _peak_detection.get_fundamental_freq(
		x_arr,
		freq_arr,
		ctypes.c_size_t(N),
		ctypes.c_float(threshold)
	)
	return float(result)



def test():
	import time
	import numpy as np
	import matplotlib.pyplot as plt

	def bins_to_freq(sample_rate, N):
		return [i*(sample_rate/N) for i in range(N)]

	def generate_time_arr(t_start, t_stop, sample_rate, maxsize):
		t_step = 1/sample_rate

		t_arr = []
		t = t_start
		i = 0
		while (t < t_stop) and (i < maxsize):
			t_arr.append(t)

			t += t_step
			i += 1

		return t_arr


	bins = 1 << 15
	sample_rate = 44.1E3
	
	t_arr = generate_time_arr(0, 5, sample_rate, bins)

	freq = 440
	w = 2*np.pi*freq
	x = [np.sin(w*t) + np.sin((w/2)*t) + np.sin(2*w*t) for t in t_arr]
	
	freqs = bins_to_freq(sample_rate, bins)

	start_time = time.time()

	X = fft(x)
	print(f"Elapsed time = {time.time() -  start_time}")

	f = get_fundamental_freq(X, freqs, 5)
	print(f"Fundamental freq = {f}")


	plt.plot(freqs, X)
	plt.show()


if __name__ == "__main__":
	test()