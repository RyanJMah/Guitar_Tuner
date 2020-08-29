import os
import csv
import numpy as np
import matplotlib.pyplot as plt

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIRECTORY, "dft_data.csv")) as f:
	reader = csv.reader(f)
	data = list(reader)

data = [float(i[0]) for i in data]

f = 440
T = 1/f
time_samples = []
for i in range(len(data)):
	time_samples.append(i*T)

plt.plot(time_samples, data)
plt.show()

