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

	#Set up filter to be at least twice as long as input
	m = np.ceil(np.log(2*n-1) / np.log(2))
	m = int(2 ** m)

	#Create ramp filter
	wmax=1/(2*scale)
	print(wmax)
	size=math.floor(2*wmax)
	timestep=2*wmax/m
	w=np.fft.fftfreq(math.floor(size/timestep))
	#w=np.linspace(-wmax,wmax, m)
	ramp=np.abs(w)*timestep
	#print(ramp.shape)
	print(m)
	#ramp1=ramp
	#ramp1[:int(m/2)]=ramp[int(-m/2):]
	#ramp1[int(m/2)+1:]=np.flip(ramp[:int(m/2)]) #fft freq

	# Create raised cosine filter
	#raised_cos=np.abs(w)*(np.cos(w/2*m))**alpha
	#raised_cos[0]=raised_cos[1]/6 #1/6th of 1st value

	plt.plot(ramp)
	#raised_cos1=raised_cos
	#raised_cos1[:int(m/2)]=raised_cos[int(-m/2):]
	#raised_cos1[int(m/2):]=np.flip(raised_cos[:int(m/2)])
	#plt.plot(raised_cos1)


	# apply filter to all angles
	print('Ramp filtering')
	for i in range(angles):
		Fsinogram=np.fft.fft(sinogram[i],m)
		#print(ramp.shape,Fsinogram.shape)
		Fproduct=ramp*Fsinogram
		product=np.real(np.fft.ifft(Fproduct)[:n])
		sinogram[i]=product


	return sinogram