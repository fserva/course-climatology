#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Setup parameters and constants
make_maps = False  # Show global maps
make_ts   = True   # Show zonal averages
dgrid = 2.5        # ERBE data resolution (degrees)
r_e = 6.371*1E6    # Earth radius (m)

# Define a Basemap object for plotting
def map_setup(lon1,lon2,lat1,lat2,col_con,col_lake,col_sea,col_bound):
    mymap = Basemap(projection='cyl',llcrnrlon=lon1, urcrnrlon=lon2, \
            llcrnrlat=lat1, urcrnrlat=lat2, \
            lon_0=0, lat_0=0, resolution='c')
    # Add coastlines, meridian and parallel lines 
    mymap.drawcoastlines(color=col_bound,linewidth=.35)
    mymap.drawmeridians(np.arange(0,360,30),color='gray',linewidth=.25)
    mymap.drawparallels(np.arange(-90,90,30),color='gray',linewidth=.25)
    return mymap


# *** Lat/Lon global maps ***
data_path = './radiation_data/' # CHANGEME
"""
 9  CLEAR-SKY NET RADIATION                                           
10  CLEAR-SKY ALBEDO                                                  
11  LONGWAVE CLOUD FORCING                                            
12  SHORTWAVE CLOUD FORCING                                           
13  NET CLOUD FORCING        
"""

# Open ERBE year/month 2D data, and select columns
erbe_2d = np.genfromtxt(data_path+'ERBE_01_1987.txt',\
                        skip_header=19,dtype='str',delimiter='?')

lat_2d = np.array([float(row.split()[0]) for row in erbe_2d],dtype='f') 
lon_2d = np.array([float(row.split()[1]) for row in erbe_2d],dtype='f')

# Shortwave radiation (reflected)
sw_2d =  np.array([float(row.split()[2]) for row in erbe_2d],dtype='f')
sw_2d[np.where(sw_2d == 999.99)] = float('nan')

# Longwave radiation
lw_2d =  np.array([float(row.split()[3].split('-')[0]) 
                  for row in erbe_2d],dtype='f')
#net_2d =  np.array([float(row.split()[1]) for row in erbe_2d],dtype='f')

# Albedo
alb_2d =  np.array([float(row.split()[5]) for row in erbe_2d],dtype='f')
alb_2d[np.where(alb_2d == 0.0)] = float('nan') # suspect
alb_2d[np.where(alb_2d == 999.99)] = float('nan')

# Clear-sky quantities
#cssw_2d =  np.array([float(row.split()[1]) for row in erbe_2d],dtype='f')
#cslw_2d =  np.array([float(row.split()[1]) for row in erbe_2d],dtype='f')
#csa_2d =  np.array([float(row.split()[1]) for row in erbe_2d],dtype='f')

# Define regular lon/lat grid at 2.5 deg step
lon_rg = np.linspace(0,357.5,int(360/2.5))
lat_rg = np.linspace(-90,90,int(180/2.5)+1)

# Define regridded variables
sw_rg  = np.zeros((len(lon_rg),len(lat_rg)),dtype='f')
lw_rg  = np.zeros((len(lon_rg),len(lat_rg)),dtype='f')
alb_rg = np.zeros((len(lon_rg),len(lat_rg)),dtype='f')

# Fill with missing values to start
sw_rg[:]  = float('nan')
lw_rg[:]  = float('nan')
alb_rg[:] =  float('nan')

# Reshape into bidimensional array
for ind in range(len(lat_2d)):

    # Get the current indices
    lon_ind = np.abs(lon_rg-lon_2d[ind]).argmin()    
    lat_ind = np.abs(lat_rg-lat_2d[ind]).argmin()    

    # Assign the corresponding values
    sw_rg[lon_ind,lat_ind]  = sw_2d[ind]
    lw_rg[lon_ind,lat_ind]  = lw_2d[ind]
    alb_rg[lon_ind,lat_ind] = alb_2d[ind]

# Compute incoming shortwave
sw_in=100.*sw_rg/alb_rg 
#((100.-alb_rg)/alb_rg)*sw_rg ??

if make_maps is True:

    alb_levs = np.linspace(0,50,11)
    sw_levs  = np.linspace(50,250,11)
    in_levs  = np.linspace(200,500,11)
    abs_levs = np.linspace(100,400,11)
    #lw_levs  = ... TODO

    plt.figure()
    map_setup(0,360,-90,90,'none','none','none','black')
    plt.contourf(lon_rg,lat_rg,alb_rg.T,
                 levels=alb_levs,cmap='Blues_r',extend='max')
    plt.colorbar(orientation='horizontal')
    plt.title('Albedo [%]')

    plt.figure()
    map_setup(0,360,-90,90,'none','none','none','black')
    plt.contourf(lon_rg,lat_rg,sw_rg.T,
                 levels=sw_levs,cmap='Oranges_r',extend='max')
    plt.colorbar(orientation='horizontal')
    plt.title('Reflected SW [W/m2]')

    plt.figure()
    map_setup(0,360,-90,90,'none','none','none','black')
    plt.contourf(lon_rg,lat_rg,sw_in.T,
                 levels=in_levs,cmap='Oranges',extend='max')
    plt.colorbar(orientation='horizontal')
    plt.title('Incoming SW [W/m2]')

    plt.figure()
    map_setup(0,360,-90,90,'none','none','none','black')
    plt.contourf(lon_rg,lat_rg,(sw_in*(100-alb_rg)/100).T,
                 levels=abs_levs,cmap='Oranges',extend='max')
    plt.colorbar(orientation='horizontal')
    plt.title('(1-A) SW [W/m2]')






# *** Zonally averaged quantities *** 
# Dims: lat, month, annual mean (14 columns)
net_1d  = np.array(np.loadtxt(data_path+'NET1986.txt',skiprows=1))
olr_1d  = np.array(np.loadtxt(data_path+'OLR1986.txt',skiprows=1))
alb_1d  = np.array(np.loadtxt(data_path+'ALB1986.txt',skiprows=1))
sw_1d   = np.array(np.loadtxt(data_path+'SW1986.txt',skiprows=1))
lat_1d  = np.array(net_1d[:,0])
lat_wgt = np.cos(lat_1d*np.pi/180.)*r_e*r_e*(dgrid*np.pi/180.)


# Prepare monthly time series
net_ts = np.zeros(12,dtype='f')
sw_ts  = np.zeros(12,dtype='f')
olr_ts = np.zeros(12,dtype='f')
alb_ts = np.zeros(12,dtype='f')
abs_ts = np.zeros(12,dtype='f')


for mon in range(12):
   net_ts[mon] = np.sum(net_1d[:,mon+1]*lat_wgt)/np.sum(lat_wgt)
   olr_ts[mon] = np.sum(olr_1d[:,mon+1]*lat_wgt)/np.sum(lat_wgt)
   sw_ts[mon]  = np.sum(sw_1d[:,mon+1]*lat_wgt)/np.sum(lat_wgt)

   ind_mon = np.where(alb_1d[:,mon+1] > 0)
   abs_ts[mon] = np.sum(sw_1d[ind_mon,mon+1]/alb_1d[ind_mon,mon+1]*\
                 (100.-alb_1d[ind_mon,mon+1])*lat_wgt[ind_mon])/np.sum(lat_wgt[ind_mon])


ind_ann = np.where(alb_1d[:,13] > 0) # Exclude missing values
abs_ann = np.squeeze(sw_1d[ind_ann,13]/alb_1d[ind_ann,13]*(100.-alb_1d[ind_ann,13]))

if make_ts is True:
    plt.figure()
    abs_anom = abs_ts - np.mean(abs_ts)
    olr_anom = -olr_ts + np.mean(olr_ts)
    plt.plot(1+np.arange(12),net_ts,label='net')
    plt.plot(1+np.arange(12),abs_anom+olr_anom,label="abs' + olr'")
    plt.plot(1+np.arange(12),abs_anom,label="abs'")
    plt.plot(1+np.arange(12),olr_anom,label="olr'")
    plt.ylim([-20,20])
    plt.xlabel('Month')
    plt.ylabel('Avg flux [W/m2]')
    plt.axhline(0,color='k')
    plt.legend()

    plt.figure()
    plt.plot(lat_1d,abs_ann,label='abs')
    plt.plot(lat_1d,olr_1d[:,13],label='olr')
    plt.plot(lat_1d,net_1d[:,13],label='net')
    # Effects of correction
    plt.plot(lat_1d,abs_ann-olr_1d[:,13],label='abs-olr')
    plt.xlabel('Latitude [deg]')
    plt.ylabel('Flux [W/m2]')
    plt.axhline(0,color='k')
    plt.legend()



plt.show()

