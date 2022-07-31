import numpy as np
import matplotlib.pyplot as plt
from gen_sig import sig_gen

def corr_data(arr):
	pass

def get_data(arr, osr):
	arr = np.reshape(arr, (-1,80*osr))

	ltss = arr[:2]
	arr = arr[2:]
	ret_data = np.array([])
	for frame in arr:
		frame = frame[16*osr:]
		frame_ft = np.fft.fft(frame)
		ret_data = np.append(ret_data, frame_ft)
		plt.scatter(np.real(frame_ft), np.imag(frame_ft))
		plt.show()
	return ret_data

def unmap_bpsk(arr):
	#arr = np.delete(arr)
	out_arr = np.array([])
	for num in arr:
		if np.abs(num) > .5:
			angle = np.arctan2(np.imag(num), np.real(num))
			if angle < 1.5708 and angle > -1.5708:
				out_arr = np.append(out_arr, 1)
			else:
				out_arr = np.append(out_arr, 0)
	return out_arr



osr = 4
gen = sig_gen()
sig = gen.create_signal(4)
sig = gen.add_conv(sig)
sig = gen.add_noise(sig, .005)
sig = gen.add_echo(sig, 1)

data = get_data(sig, osr)
bits = unmap_bpsk(data)
print(len(bits))
print(bits)
