import numpy as np
import matplotlib.pyplot as plt

class sig_gen():

	
	def get_lts(self, osr, cp = False):
		lts = np.array([0,1,-1,1,1,0,0,-1,0,1,1,0,0,0,1,-1,1,1,0,0,1,1,0,-1,0,1,0,0,0,1,1,-1,0,1,0,0,0,1,-1,1,1,0,0,1,0,0,-1,-1,1,1,0,1,0,0,-1,1,-1,0,0,0,-1,-1,1,1])
		#lts_ift = np.fft.ifftshift(np.fft.ifft(lts, n = 64*osr))
		lts_ift = np.fft.ifft(lts, n = 64*osr)
		
		if cp:
			lts_ift = np.append(lts_ift, lts_ift[-16*osr:])
			lts_ift = np.roll(lts_ift, 16*osr)
	
		return lts_ift
		
	
	def mod_bpsk(self, arr):
		out_arr = np.array([])
		for i in arr:
			if i == 0:
				out_arr = np.append(out_arr, complex(-1,0))
			else:
				out_arr = np.append(out_arr, complex(1,0))
		return out_arr
	
	def frame_f(self, arr_48):
		#This function will take an array of size 48 and add 4 pilots at 
		#-7, -21, 7, 21
		#it will append zeros onto the ends so the total length is 64. There will also be a zero added to index 0
		ret_arr = np.insert(arr_48, 0, [0]*6)
		ret_arr = np.insert(ret_arr, len(ret_arr), [0]*6)
		ret_arr = np.insert(ret_arr, [-6,-19,7,20], complex(1,1))
	
		return ret_arr
	
	def frame_all(self, modded_bits, osr=4):
		#This function will take an array of modulated bits
		#And output an array of frames concatenated together
		#It will also add the LTSs to the beginning
		n_zeros_append =48 - len(modded_bits)%48
		if n_zeros_append != 48:
			modded_bits = np.append(modded_bits, [0]*n_zeros_append)
		#print(len(modded_bits))
		frames = np.reshape(modded_bits, (-1,48))
		out_arr = np.array([])
		
		#append LTS here
		lts = self.get_lts(osr, cp = True)
		out_arr = np.append(out_arr, lts)
		out_arr = np.append(out_arr, lts)
	
		for frame in frames:
			frame = self.frame_f(frame)
			#NOTE, you may have to do ifftshift here somewhere
			#frame should be length 64 here, append CP of size 16 to make it size 80
			frame = np.fft.ifft(frame, n = 64*osr)
			#frame = np.fft.ifftshift(np.fft.ifft(frame, n = 64*osr))
			frame = np.append(frame, frame[-16*osr:])
			#print(len(frame))
			frame = np.roll(frame, 16*osr)
			out_arr = np.append(out_arr, frame)
		
		return out_arr
	
	def create_signal(self, osr):
		#send_bits = np.random.randint(0, high = 2, size = 70)
		send_bits = np.array([1]*48)
		bp_bits = self.mod_bpsk(send_bits)
		send_sig = self.frame_all(bp_bits, osr)
		#print(len(send_sig))
		return send_sig
	
