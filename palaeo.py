#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Location of the txt files. Adapt as needed.
data_path = './palaeo_data/'

# Open EPICA deuterium data skipping header
# 6 columns: Top depth, bottom depth, top age, bottom age, mean age, dD
epica_2h_1 = np.loadtxt(data_path+'EpicaDeuteriumPart1.txt',skiprows=96)
# 3 columns: Top age, bottom age, dD
epica_2h_2 = np.loadtxt(data_path+'EpicaDeuteriumPart2.txt',skiprows=89)

# Open pre-processed Zachos data
# 3 columns: age, raw, smoothed data
zachos_c13 = np.loadtxt(data_path+'ZachosC13Processed.txt',skiprows=9)
zachos_o18 = np.loadtxt(data_path+'ZachosO18Processed.txt',skiprows=10)

# Open Vostok T & CO2
# 2 columns: age, data
vostok_t = np.loadtxt(data_path+'vostokT.txt',skiprows=116)
# 4 columns: depth, corrected ice age, deuterium, deltaT
vostok_co2 = np.loadtxt(data_path+'vostokCO2.txt',skiprows=1)

# Open EPICA CO2
# 4 columns: depth, gas age, co2 (ppmv), sigma mean
epica_co2 = np.loadtxt(data_path+'EPICACO2.txt',skiprows=1)

# Open insolation data of Berger 1990
# 9 columns: time, eccentricity, omega, obliquity, precession, 65N Jul, 15N Jul, 15S Jan
orbit = np.loadtxt(data_path+'orbit91',skiprows=2)


# Basic FFT function
def fft(time,ts):

    # Length of the real-fft transform
    if ((len(time) % 2) == 0):
        nfreqs = int(len(time)/2) + 1 
    else:
        nfreqs = int(len(time) + 1)/2

    fft_ts = np.zeros(nfreqs,dtype='float')

    # r-fft calculation
    fft_ts = np.fft.rfft(ts) 

    # Normalization
    fft_ts /= nfreqs

    # Corresponding frequencies are: 0, 1/N*T,2/N*T,...(nfreqs-1)/(N*T)
    # where N is the number of points and T is the sampling frequency inverse.
    # Ordering is from the smaller to the larger frequency.
    fft_freq = np.fft.rfftfreq(len(time), d = (time[1]-time[0]))

    return fft_freq, np.abs(fft_ts)


# Perform the analyses on the data. 
# When data is shifted, units have a minus;
# when data is scaled, units have an asterisk

plt.figure(figsize=(8,8))

grid = plt.GridSpec(5, 4, wspace=0.6, hspace=0.8)

# Zachos oxygen isotope
plt.subplot(grid[0, 0:])
plt.plot(zachos_o18[:,0],zachos_o18[:,2],color='k')
plt.xlabel('mya')
plt.ylabel('Delta 18O')
plt.xlim([0,60])

# Vostok & EPICA
plt.subplot(grid[1, 0:])
plt.plot(vostok_co2[:,0]/1E3,vostok_co2[:,1]-200,label='Vostok CO2 - 200',color='k')
plt.plot(epica_co2[:,1]/1E3,epica_co2[:,2]-200,label='EPICA CO2')
plt.plot(vostok_t[:,1]/1E3,vostok_t[:,3]*5,label='Vostok T x 5')
plt.ylim([-50,100])
plt.xlim([0,5E2])
plt.xlabel('kya')
plt.ylabel('[ppmv-] & [K*]')


plt.subplot(grid[2, 0:2])
plt.plot(vostok_co2[:,0]/1E3,vostok_co2[:,1]-200)
plt.plot(vostok_t[:,1]/1E3,vostok_t[:,3]*5)
plt.xlim([0,2E2])
plt.xlabel('kya')
plt.ylabel('[ppmv-] & [K*]')

# Interpolate vostok data for the next plot
plt.subplot(grid[2, 2:])
vostok_t_int = np.interp(vostok_co2[:,0],vostok_t[:,1],vostok_t[:,3])
plt.plot(vostok_t_int,vostok_co2[:,1],linestyle='',marker='x',color='k')
plt.ylim([180,300])
plt.xlim([-10,5])
plt.xlabel('T [K]')
plt.ylabel('CO2 [ppmv]')
plt.title('Vostok')

plt.subplot(grid[3,0:])
plt.plot(vostok_co2[:,0]/1E3,vostok_co2[:,1]*1.5)
plt.plot(-orbit[:,0],orbit[:,5])
plt.xlim([0,5E2])
plt.xlabel('kya')
plt.ylabel('[K*] & [W/m2]')

# Plot with orbital frequency analysis
plt.subplot(grid[4,0:])
orbit_freq, ecc_fft = fft(-orbit[:,0],orbit[:,1])
orbit_freq, obl_fft = fft(-orbit[:,0],orbit[:,3])
orbit_freq, pre_fft = fft(-orbit[:,0],orbit[:,4])
plt.plot(orbit_freq[1:],ecc_fft[1:],color='b',label='ecc')
plt.plot(orbit_freq[1:],obl_fft[1:],color='k',label='obl')
plt.plot(orbit_freq[1:],pre_fft[1:],color='r',label='prec')
plt.yscale('log',basey=10)
plt.xscale('log',basex=10)
plt.xlim([1e-3,1e-1])
plt.ylim([1E-5,1])
plt.xlabel('Freq [kyr-1]')
plt.legend()

plt.show()



