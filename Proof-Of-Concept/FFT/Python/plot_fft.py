import os
import sys

# from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

THIS_DIRECTORY = os.path.dirname(__file__)


def plot_FT(Af, sample_rate):
    N = len(Af)

    Af = Af[:int(N/2)]
    # thing = [abs(i) for i in Af]
    f = [i*(sample_rate/N) for i in range(int(N/2))]

    print(f[Af.index(max(Af))])

    plt.grid()
    plt.plot(f, Af)
    # plt.scatter(f, Af)
    plt.show()
    plt.close()


if __name__ == "__main__":
    with open(os.path.join(THIS_DIRECTORY, "dft_data.csv"), "r") as f:
        reader = csv.reader(f)

        data = list(reader)
        data = [float(i[0]) for i in data]

    plot_FT(data, 1024*10)



