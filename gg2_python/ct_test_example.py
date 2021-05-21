
# import necessary modules
import numpy as np
from material import *
from source import *
from fake_source import *
from ct_phantom import *
from ct_lib import *
from scan_and_reconstruct import *
from create_dicom import *

# create object instances
material = Material()
source = Source()

# End-to-end tests defined below
# all the outputs are saved in a 'results' directory

def test_1():
	# Test 1 saves images for phantom and reconstruction to results directory
	# Can visually compare geometry

	# Setting up scenario for comparison
	# Single hip replacement phantom generated
	p = ct_phantom(material.name, 256, 3)
	s = source.photon('100kVp, 3mm Al') # Could be tried with different energy sources
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# Results saved to 2 separate files 
	save_draw(y, 'results', 'test_1_image')
	save_draw(p, 'results', 'test_1_phantom')
	# Check geometries appear similar 
	# Typically some differences in images, partly due to scanning and reconstruction artefacts,
	#  as well as colour scaling due to phantom using material indexing and reconstruction using linear attenuation coefficients
	# Also get dark corners where scan doesn't reach due to circular nature of scanning
	

def test_2():
	# Test 2 plots normalised values for phantom and reconstruction along single line through centre of images
	# Plotted both separately and overlaid for visual comparison

	# Setting up scenario for comparison
	# Single hip replacement phantom generated
	p = ct_phantom(material.name, 256, 3)
	s = source.photon('80kVp, 1mm Al') # Could be tried with different energy sources
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# Find maximum value in image for normalisation
	max_y=np.max(y)
	max_p=np.max(p)

	# Individual plots saved
	save_plot(y[127,:], 'results', 'test_2_y_plot')
	save_plot(p[127,:], 'results', 'test_2_p_plot')
	# Results plotted together for direct comparison
	plt.plot(y[127,:]/max_y)
	plt.plot(p[127,:]/max_p)
	plt.title("Comparing data values on 128th row for phantom and reconstruction")
	plt.legend(['reconstruction','phantom'])
	plt.ylabel('Normalised linear attenuation')
	plt.xlabel('Bin index')
	full_path = get_full_path('results', 'test_2_combined_plot')
	# Overlaid plot saved to results directory
	plt.savefig(full_path)
	plt.close()

	# Normalisation is purely for ease of comparison, accurate reconstruction can be tested by checking if peaks line up


def test_3():
	# Test 3 compares mean value across central area (bins 65 to 193) to known linear attuenuation coefficient for single energy, extracted from mass_attenuation_coeffs spreadsheet

	# Disc phantom generated
	# Ideal source used to get single energy photons
	p = ct_phantom(material.name, 256, 1)
	s = fake_source(source.mev, 0.1, method='ideal')
	y = scan_and_reconstruct(s, material, p, 0.1, 256)
	
	# Retrieve linear attenuation coefficients for default material, which is soft tissue for phantom scenario 1
	coeffs=material.coeff('Soft Tissue')
	energies=material.mev
	# Find index for required energy, which will be 70% of energy given as mvp in fake_source
	i = np.where(energies==0.07)
	# Find lin att coeff corresponding to single energy
	value=coeffs[i]
	# Calculate mean
	mean=np.mean(y[64:192, 64:192])

	# Results saved to text file
	f = open('results/test_3_output.txt', mode='w')
	f.write('Mean value of small square in middle is: ' + str(np.mean(y[64:192, 64:192])) + '\n')
	f.write('The true value obtained from material linear attenuation coefficient is: ' + str(float(value)) + '\n')
	# Calculate and show percentage difference between values
	f.write('Giving a percentage difference of: ' + str(np.float(100*abs((mean-value)/value))) + '%' + '\n')
	f.close()

	# Run test with error catching to identify if test fails
	try:
		diff=abs((mean-value)/value)
		# Margin for success set to 10%
		assert diff<0.1
		message="Test 3 Successful"
	except AssertionError:
		message="Test 3 Failed"

	print('Mean: ' + str(mean))
	print('Value: ' + str(float(value)))
	print('Percentage difference: ' + str(float(diff*100))+"%")
	print(message)
	f = open('results/test_3_output.txt', mode='a')
	# Print whether test is successful to file
	f.write(message)
	f.close()


def test_4():
	# Test 4 compares location of peak values, which should be in the centre when using single point phantom

	# Single point phantom generated
	p = ct_phantom(material.name, 256, 2)
	s = source.photon('100kVp, 3mm Al') # Could be tried with different energy sources
	y = scan_and_reconstruct(s, material, p, 0.01, 256)

	# Find max values within images
	max_y=np.max(y)
	max_p=np.max(p)
	# Retrieve locations for maximum points
	max_y_ind=np.where(y==max_y)
	max_p_ind=np.where(p==max_p)

	# Write locations of both maxima to text file
	f = open('results/test_4_output.txt', mode='w')
	f.write("Max value in phantom is at: "+str(np.asarray(max_p_ind[0]))+', '+str(np.asarray(max_p_ind[1]))+"\n Max value in reconstruction is at: "+str(np.asarray(max_y_ind[0]))+', '+str(np.asarray(max_y_ind[1])) + "\n")
	f.close()

	# Run test with error catching to identify if test fails
	try:
		# Maxima must be at same location for test to pass
		assert max_y_ind==max_p_ind
		message="Test 4 Successful"
	except AssertionError:
		message="Test 4 Failed"
	
	print('Max in reconstruction at: ' +str(np.asarray(max_y_ind[0]))+', '+str(np.asarray(max_y_ind[1])))
	print('Max in phantom at: ' +str(np.asarray(max_p_ind[0]))+', '+str(np.asarray(max_p_ind[1])))
	print(message)
	f = open('results/test_4_output.txt', mode='a')
	# Print whether test is successful to file
	f.write(message)
	f.close()







# Run the various tests
print('Test 1')
test_1()
print('Test 2')
test_2()
print('Test 3')
test_3()
print("Test 4")
test_4()
