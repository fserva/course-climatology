#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys # warning: only works from command line, no spyder or notebook!

""" 
Based on Pierrehumbert's script for ice-albedo
feedbacks, with some simplifications (e.g. no bifurcation
diagram is prepared)

v 0.1: first version April 2019
"""

# Read the solar constant (W/m2), if provided
if len(sys.argv) == 1:
    l_o = 1300.

if len(sys.argv) > 1:
    l_o = int(sys.argv[1])

# Constant and setup parameters
blackbody = True
tlen = 200 # number of temperature increments
plen = 20 # number of pressure increments
pincr = 30 # step for pressure increments (mbar)
n_eq = 3 # number of equilibria
alpha_i = 0.6 # ice albedo
alpha_o = 0.1 # water albedo
#l_o = 1300. # solar constant (W/m2)
sigma = 5.67*1E-08 # Boltzmann's constant
rcp = 0.278 # R/cp
temp_i = 260. # ice temperature
temp_o = 290. # water temperature
olr_a = 113. #
olr_b = 2.177

# Array definition
temp = 150. + np.arange(tlen)
alpha = np.zeros(tlen,dtype='f')
olr = np.zeros(tlen,dtype='f')
eq_pts = np.zeros((n_eq,plen),dtype='i')

# Compute albedo as function of temperature
alpha[np.where(temp < temp_i)[0]] = alpha_i
alpha[np.where(temp > temp_o)[0]] = alpha_o
cond_mix = np.where(np.logical_and(temp >= temp_i, temp <= temp_o))
alpha[cond_mix] = alpha_o + (alpha_i-alpha_o)*((temp[cond_mix]-temp_o)/(temp_o-temp_i))**2

plt.figure(figsize=(5,6))
plt.subplot(3,1,1)
plt.plot(temp,alpha)
plt.xlabel('Surface temperature (K)')
plt.ylabel('alpha (adim)')


flux_in = l_o*(1-alpha)*0.25
flux_out = sigma*temp**4
prad = 900 - np.arange(plen)*pincr

plt.subplot(3,1,2)
plt.plot(temp,flux_in,'k',zorder=10,label='in')

# Loop over pressures
for ipress in range(plen):

    if blackbody is True: 
        flux_rad = sigma*(temp/(1000./prad[ipress])**rcp)**4
        plt.title('L = '+str(l_o)+' (varying prad)')

    else:
        flux_rad = olr_a + olr_b*(temp-220.)
        plt.title('L = '+str(l_o)+' (linear approx)') 

    flux_net = flux_in - flux_rad
    radlab = 'out'
    if ipress != 0: radlab = None
    plt.plot(temp,flux_rad,color='red',ls='--',label=radlab)
    n_eq = 0
    for itemp in range(tlen-1):
        if flux_net[itemp]*flux_net[itemp+1] < 0.:
            eq_pts[n_eq,ipress] = itemp
            n_eq += 1

plt.ylim([50,350])
plt.xlabel('Surface temperature (K)')
plt.ylabel('Flux (W/m2)')
plt.legend()

plt.subplot(3,1,3)
if blackbody is True:
    plt.plot(prad,temp[np.squeeze(eq_pts[0,:])],ls='',marker='*',color='b')
    plt.plot(prad,temp[np.squeeze(eq_pts[1,:])],ls='',marker='*',color='grey')
    plt.plot(prad,temp[np.squeeze(eq_pts[2,:])],ls='',marker='*',color='r')
    plt.xlim([max(prad),min(prad)])
    plt.ylim([200,350])
    plt.axhline(temp_i,color='b')
    plt.axhline(temp_o,color='r')
    plt.xlabel('Prad (mbar)')
    plt.ylabel('Eq temp (K)')
else:
    plt.text(0.3,0.5,'No prad dependence')

plt.tight_layout()
plt.show()
#plt.savefig('CHANGEME.png',format='png') # save png, change name as needed

