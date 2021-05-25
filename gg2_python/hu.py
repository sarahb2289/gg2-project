import numpy as np
from attenuate import *
from ct_calibrate import *

def hu(p, material, reconstruction, scale):
	""" convert CT reconstruction output to Hounsfield Units
	calibrated = hu(p, material, reconstruction, scale) converts the reconstruction into Hounsfield
	Units, using the material coefficients, photon energy p and scale given."""

	n=p.shape[0]
	# print(p.shape,reconstruction.shape,len(material.coeff('Water')))
	depth=2*n*scale
	print(depth)
	# use water to calibrate
	p_water = attenuate(p,material.coeff('Water'),depth)
	p_water_tot=np.sum(p_water)
	print(p_water_tot)
	# print(p_water.shape,reconstruction.shape, p_water_ave)
	# put this through the same calibration process as the normal CT data
	airscan=attenuate(p,material.coeff('Air'),depth)
	# Sum along path to get total energy according to eq 3 from handout
	Io=np.sum(airscan)
	# print(Io)
	mu_water_ave=-np.log(p_water_tot/Io)
	print(mu_water_ave/depth)
	# mu_water=ct_calibrate(p,material,p_water_sum,scale)
	# print(mu_water_ave)
	# print(reconstruction[:,10])
	# use result to convert to hounsfield units
	hreconstruction = 1000*(reconstruction-(mu_water_ave/depth))/(mu_water_ave/depth)
	# limit minimum to -1024, which is normal for CT data.
	for i in range(hreconstruction.shape[0]):
		for j in range(hreconstruction.shape[1]):
			# print(hreconstruction[i,j])
			if hreconstruction[i,j]<-1024.0:
				hreconstruction[i,j]=-1024.0

	return hreconstruction

	