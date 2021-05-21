import math
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt

def ramp_filter(sinogram, scale, alpha=0.001):
	""" Ram-Lak filter with raised-cosine for CT reconstruction

	fs = ramp_filter(sinogram, scale) filters the input in sinogram (angles x samples)
	using a Ram-Lak filter.

	fs = ramp_filter(sinogram, scale, alpha) can be used to modify the Ram-Lak filter by a
	cosine raised to the power given by alpha."""

	# get input dimensions
	angles = sinogram.shape[0]
	n = sinogram.shape[1]

	#Set up filter to be at least twice as long as input to avoid issues with circular convolution
	m = np.ceil(np.log(2*n-1) / np.log(2))
	m = int(2 ** m)

	#Create ramp filter

	# Calculate maximum frequency, which will be equal to Nyquist frequency in order to avoid aliasing
	wmax=1/(2*scale)
	# Retrieve set of frequencies that match format for fft (length m and interval scale)
	w=np.fft.fftfreq(m,d=scale)
	# Create ramp equal to absolute values of frequencies 
	ramp=np.abs(w)
	# Set DC value to slightly above zero
	ramp[0]=1/6*ramp[1]


	# Create raised cosine filter

	# Create raised cosine filter according to eq 14 from handout
	raised_cos1=np.abs(w)*((np.cos(w/(2*m))))**alpha
	# Set DC value to slightly above zero
	raised_cos1[0]=(raised_cos1[1])/6 


	# apply filter to all angles
	print('Ramp filtering')
	for i in range(angles):
		# Take fourier transform to allow multiplication in frequency domain rather than convolution in time domain
		# Convolution is more computationally expensive
		# fft function adds zero padding to make output length match filter array
		Fsinogram=np.fft.fft(sinogram[i],m)
		#Fproduct=ramp*Fsinogram #Can choose between using pure ramp filter or raised cosine filter
		Fproduct=raised_cos1*Fsinogram 
		# Inverse fourier transform to move back into time domain, only keep real part to discard any effects of non-ideality
		product=np.real(np.fft.ifft(Fproduct)[:n]) # Only take first n values from m length array
		sinogram[i]=product


	return sinogram