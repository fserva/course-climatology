
import numpy as np
import matplotlib.pyplot as plt

population = 'mix'
#population = 'neutral'
#population = 'black'
#population = 'white'

l_o = 1400. # W/m2
sigma = 5.67*1E-08 # Boltzmann constant
dt = 1 # delta for time
dl = 2*1E-04 # delta for solar 'constant'
ns = 5000 # number steps

# Define array of solar constants
l_a = (0.2+np.arange(ns)*dl)*l_o

# Albedos (black, white, bare soil)
if population == 'mix':
    bd_a = 0.25
    wd_a = 0.75
    bs_a = 0.50

if population == 'neutral':
    bd_a = 0.50
    wd_a = 0.50
    bs_a = 0.50

if population == 'black':
    bd_a = 0.25
    wd_a = 0.25
    bs_a = 0.50

if population == 'white':
    bd_a = 0.75
    wd_a = 0.75
    bs_a = 0.50


# Variables
t_bd = np.zeros(ns,dtype='f') # black daisies temp
t_wd = np.zeros(ns,dtype='f') # white daisies temp
bd   = np.zeros(ns,dtype='f') # black daisies fraction
wd   = np.zeros(ns,dtype='f') # white daisies fraction
xx   = np.zeros(ns,dtype='f') # bare ground fraction
aa   = np.zeros(ns,dtype='f') # Daisyworld albedo
t_d  = np.zeros(ns,dtype='f') # Daisyworld temp
bdg  = np.zeros(ns,dtype='f') # black daisies growth
wdg  = np.zeros(ns,dtype='f') # white daisies growth


# Set initial conditions
bd[0]   = 0.01 
wd[0]   = 0.01 
xx[0]   = 1.-bd[0]-wd[0]
aa[0]   = bs_a
t_d[0]  = ((l_a[0]*(1-aa[0])/sigma)**0.25)-273.
t_bd[0] = t_d[0] 
t_wd[0] = t_d[0]


# Loop over time
it = 1
while it < ns:
    qq = 0.2 * l_a[it] / sigma
    gam = 0.3

    # Let the two population evolve. 
    # ??b = growth function, ??g = growth rate, ??d = death rate
    # Cap the fractions to avoid extinction

    # Black daisies
    bd_b = 0.
    if np.logical_and(t_bd[it-1] > 5,t_bd[it-1] < 40):
        bd_b = 1 - 0.003265*((22.5-t_bd[it-1])**2)
    bdg[it] = bd[it-1]*bd_b*xx[it-1]
    bdd = bd[it-1]*gam
    bd[it] = bd[it-1] + (bdg[it]-bdd)*dt
    if bd[it] < 0.01: bd[it] = 0.01


    # White daisies
    wd_b = 0.
    if np.logical_and(t_wd[it-1] > 5, t_wd[it-1] < 40):
        wd_b = 1 - 0.003265*((22.5-t_wd[it-1])**2)
    wdg[it]  = wd[it-1]*wd_b*xx[it-1]
    wdd = wd[it-1]*gam
    wd[it] = wd[it-1] + (wdg[it]-wdd)*dt
    if wd[it] < 0.01: wd[it] = 0.01

    # Bare soil and planetary albedo calculation
    xx[it] = 1. - bd[it] - wd[it]
    aa[it] = (xx[it]*bs_a) + (bd_a*bd[it]) + (wd_a*wd[it])
    
    # Equilibrium
    t_d[it] = ((l_a[it]*(1-aa[it])/sigma)**0.25) - 273.
    t_wd[it] = t_d[it]
    t_bd[it] = t_d[it]

    if wd[it] > 0.01:
        t_wd[it] = ((qq*(aa[it]-wd_a)+(t_d[it]+273.)**4.)**0.25) - 273.

    if bd[it] > 0.01:
        t_bd[it] = ((qq*(aa[it]-bd_a)+(t_d[it]+273.)**4.)**0.25) - 273. 

    # Increment loop counter
    it += 1

f_out = sigma*(t_d+273.)**4.
f_in = l_a*(1-aa) 

t_neut = (l_a*(1-bs_a)/sigma)**0.25

plt.figure(figsize=(5,6))
plt.subplot(3,1,1,)
plt.plot(l_a,xx,'gray',label='bare')
plt.plot(l_a,bd,'black',label='black')
plt.plot(l_a,wd,'yellow',label='white')
plt.ylabel('Area fraction (0-1)')
plt.title(population)
plt.legend()

plt.subplot(3,1,2)
plt.plot(l_a,aa,'k')
plt.ylabel('Albedo (0-1)')

plt.subplot(3,1,3)
plt.plot(l_a,t_d,'k-',label='actual')
plt.plot(l_a,t_neut-273.,'k:',label='bare')
plt.ylabel('Temperature (degC)')
plt.xlabel('stellar luminosity (W/m2)')
plt.legend()


plt.show()


