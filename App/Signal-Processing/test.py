import time
import numpy as np
import matplotlib.pyplot as plt

from fft import fft, get_fundamental_freq

def test():
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