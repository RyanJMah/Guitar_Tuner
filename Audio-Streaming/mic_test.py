# MOST OF THIS CODE WAS NOT WRITTEN BY ME
# IT CAN BE FOUND HERE: https://gist.github.com/ZWMiller/53232427efc5088007cab6feee7c6e4c

import time
import pyaudio
import numpy as np
import pylab
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time
import os
import sys
import seaborn as sns


def heaviside(N, phase_shift = 0):
    ret = [0 for _ in range(N)]
    for i in  range(phase_shift, N):
        ret[i] = 1
    return ret

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(DIRECTORY)

sys.path.append(os.path.join(SRC_DIR, "Signal-Processing"))

from fft import *


FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = (1 << 15) # 1024bytes of data red from a buffer
RECORD_SECONDS = 0.75
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True
)


# Open the connection and start streaming the data
stream.start_stream()

audio_samples = np.frombuffer(stream.read(CHUNK), np.int16)

start = time.time()

dc_offset = np.mean(audio_samples)
print(f"df_offset = {dc_offset}")
audio_samples = [adc*(1/((1<<16) - 1)) for adc in audio_samples]  # converts adc values to voltages (assumes Vref = 1)
                                                                  # wikipedia says Vref = 1 is common so ya...

# dc_offset = np.mean(audio_samples)
# print(f"df_offset = {dc_offset}")
# audio_samples = [Vi-dc_offset for Vi in audio_samples]

# plt.plot([t for t in range(CHUNK)], audio_samples)
# plt.show()
# plt.close()

# mean = np.mean(audio_samples)
# print(f"Sum = {np.sum(audio_samples)}")
# audio_samples = [x-mean for x in audio_samples]  # convert to voltage and remove dc offset

freqs = bins_to_freq(RATE, int(len(audio_samples)))
high_pass = heaviside(int(CHUNK), 35)


X = fft(audio_samples)
X = [X[i]*high_pass[i] for i in range(int(CHUNK))]

X = harmonic_product_spectrum(freqs, X)

print(time.time() - start)



plt.plot(freqs, X)
# plt.scatter(freqs, X)
plt.show()




# print("\n+---------------------------------+")
# print("| Press Ctrl+C to Break Recording |")
# print("+---------------------------------+\n")




# Loop so program doesn't end while the stream callback's
# itself for new data
# while keep_going:
#     try:
#         plot_data(stream.read(CHUNK))
#     except KeyboardInterrupt:
#         keep_going=False
#     except:
#         pass

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()