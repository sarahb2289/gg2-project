# from material import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from ct_detect import *
def inverseE(x,k):
    y=k/x
    return y

def inverseE3(x,k):
    y=k/x**3
    return y

def plot_coeffs(energies,coeffs):
    # print(coeffs[10],coeffs[190])
    plt.plot(energies,coeffs,label='linear attenuation coefficients')
    # plt.plot(coeffs,label='original coeffs')
    plt.plot(energies,(1/energies)*coeffs[170]*energies[170],label='1/E')
    plt.plot(energies,(1/energies**3)*coeffs[5]*energies[5]**3,label='1/E^3')
    # parameters, covariance = curve_fit(inverseE,energies[180:],coeffs[180:])
    # fit_y=inverseE(energies,parameters[0])
    # plt.plot(energies, fit_y,label='fit')
    # parameters3, covariance3 = curve_fit(inverseE3,energies,coeffs)
    # fit_y3 = inverseE3(energies,parameters3[0])
    # plt.plot(energies, inverseE3(energies,fit_y3),label='fit3')
    plt.loglog()
    plt.legend()
    plt.xlabel('Energies')
    plt.ylabel('Linear Attenuation Coefficients cm^-1')
    plt.title('Linear attenuation coefficients for Titanium')
    plt.show()  

def plot_log_attenuation(p, source, coeffs, material, depths):
    y=ct_detect(p,coeffs,depths,1)
    plt.plot(depths, np.log(y))
    plt.title('Source: ' + str(source) + ', Material: ' + str(material))
    plt.xlabel('Depth')
    plt.ylabel('Residual Energy')
    plt.show()



