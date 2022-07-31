import numpy as np
import matplotlib.pyplot as plt
from gen_sig import sig_gen


def get_data(arr, osr):
	arr = np.reshape(arr, (-1,80*osr))
	for frame in arr:
		frame = frame[16*osr:]
		frame_ft = np.fft.fft(frame)
		plt.scatter(np.real(frame_ft), np.imag(frame_ft))
		plt.show()

osr = 4
gen = sig_gen()
sig = gen.create_signal(4)
get_data(sig, osr)
