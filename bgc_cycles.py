#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4

# Select the background map library
#map_type = 'nomap'
#map_type = 'basemap'
map_type = 'cartopy'

path_data = './tmp_bgc/' 

if map_type == 'basemap':

    from mpl_toolkits.basemap import Basemap
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


if map_type == 'cartopy':
    import cartopy.crs as ccrs
    def map_setup():
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180.))
        ax.coastlines()
        return ax


# Open file with all variables
yyyy0 = 2004; yyyy1 = 2013
units = {'tcco2':'ppm','tcch4':'ppb','flux':'kg m-2 s-1'}
ncf = nc4.Dataset(path_data+f'ghg_EGG4_{yyyy0}-{yyyy1}.nc','r')
lat = ncf.variables['lat'][:]
lon = ncf.variables['lon'][:]
tcco2 = ncf.variables['tcco2'][:]
tcch4 = ncf.variables['tcch4'][:]
fco2nee = ncf.variables['fco2nee'][:]
fco2oce = ncf.variables['co2of'][:]
fco2ant = ncf.variables['co2apf'][:]
ncf.close()

# Get the number of months in the file
ntim = tcco2.shape[0]


plt.figure(figsize=(6,4))

# Define contour levels for the plots
# Note these values are suitable for the full record
# until 2020
clevs_co2 = np.linspace(387,397,11)
clevs_ch4 = np.linspace(1700,1900,11)

if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

if map_type == 'cartopy': # use transform keyword
    map_setup() 
    plt.contourf(lon,lat,np.mean(tcco2,axis=0),levels=clevs_co2,
                 extend='both',transform=ccrs.PlateCarree(),cmap='PRGn_r')
    clb = plt.colorbar()
    clb.set_label(units['tcco2'])


if map_type in ['nomap','basemap']: # no transform
    plt.contourf(lon,lat,np.mean(tcco2,axis=0))

plt.figure(figsize=(6,4))

if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

if map_type == 'cartopy': # use transform keyword
    map_setup() 
    plt.contourf(lon,lat,np.mean(tcch4,axis=0),levels=clevs_ch4,
                 extend='both',transform=ccrs.PlateCarree(),cmap='PRGn_r')
    clb = plt.colorbar()
    clb.set_label(units['tcch4'])

if map_type in ['nomap','basemap']: # no transform
    plt.contourf(lon,lat,np.mean(tcch4,axis=0))


# Maps of monthly mean carbon dioxide
fig, axs = plt.subplots(nrows=3,ncols=4,figsize=(11,8.5))

# axs is a 2 dimensional array of `GeoAxes`.  We will flatten it into a 1-D array
axs=axs.flatten()

#Loop over all of the months
for imon in range(12):
    
    # Time average with N=12 stride
    data = np.mean(tcco2[imon::12],axis=0)

    # Contour plot. This assumes no projection!
    cs=axs[imon].contourf(lon,lat,data,
                          cmap='plasma',extend='both',
                          levels=clevs_co2)

    # Title each subplot with the name of the model
    axs[imon].set_title('Month = {}'.format(imon+1))

    # Draw the coastines for each subplot
    #axs[imon].coastlines()
    plt.colorbar(cs,ax=axs[imon])

plt.tight_layout()


# Compute zonal and global means, area-weighting is required
lat_wgt = np.cos(lat*np.pi/180.)
tcco2_zm = np.mean(tcco2,axis=2)
tcco2_gm = np.average(tcco2_zm,weights=lat_wgt,axis=1)
tcch4_zm = np.mean(tcch4,axis=2)
tcch4_gm = np.average(tcch4_zm,weights=lat_wgt,axis=1)

plt.figure(figsize=(9,3))
plt.subplot(1,2,1)
plt.plot(yyyy0+np.arange(ntim)/12.,tcco2_gm,'k-')
plt.xlim([yyyy0,yyyy1])
plt.ylabel(f"CO2 ({units['tcco2']})")
plt.grid()
plt.subplot(1,2,2)
plt.plot(yyyy0+np.arange(ntim)/12.,tcch4_gm,'k-')
plt.xlim([yyyy0,yyyy1])
plt.ylabel(f"CH4 ({units['tcch4']})")
plt.grid()
plt.tight_layout()


# Carbon dioxide fluxes

# Values are adjusted depending on the variable
clevs_flux = np.linspace(-5,5,11)*1.E-8

plt.figure(figsize=(6,4))

# Net ecosystem exchange
if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

if map_type == 'cartopy':
    map_setup() 
    plt.contourf(lon,lat,np.mean(fco2nee,axis=0),levels=clevs_flux,
                 extend='both',transform=ccrs.PlateCarree(),cmap='PRGn_r')
    clb = plt.colorbar()
    clb.set_label(units['flux'])
    plt.title('Net ecosystem exchange')

if map_type in ['nomap','basemap']:
    plt.contourf(lon,lat,np.mean(fco2nee,axis=0))

# Ocean fluxes
plt.figure(figsize=(6,4))

if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

if map_type == 'cartopy': # use transform keyword
    #plt.subplot(2,1,1)
    map_setup() 
    plt.contourf(lon,lat,np.mean(fco2oce,axis=0),levels=clevs_flux/10.,
                 extend='both',transform=ccrs.PlateCarree(),cmap='PRGn_r')
    clb = plt.colorbar()
    clb.set_label(units['flux'])
    plt.title('Ocean')

if map_type in ['nomap','basemap']: # no transform
    plt.contourf(lon,lat,np.mean(fco2nee,axis=0))
 
# Anthropogenic contribution
plt.figure(figsize=(6,4))

if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

if map_type == 'cartopy': # use transform keyword
    #plt.subplot(2,1,1)
    map_setup() 
    plt.contourf(lon,lat,np.mean(fco2ant,axis=0),levels=clevs_flux/10.,
                 extend='both',transform=ccrs.PlateCarree(),cmap='PRGn_r')
    clb = plt.colorbar()
    clb.set_label(units['flux'])
    plt.title('Anthropogenic')

if map_type in ['nomap','basemap']: # no transform
    plt.contourf(lon,lat,np.mean(fco2ant,axis=0))

# Time series of fluxes
fnee_zm = np.mean(fco2nee,axis=2)
fnee_gm = np.average(fnee_zm,weights=lat_wgt,axis=1)
foce_zm = np.mean(fco2oce,axis=2)
foce_gm = np.average(foce_zm,weights=lat_wgt,axis=1)
fant_zm = np.mean(fco2ant,axis=2)
fant_gm = np.average(fant_zm,weights=lat_wgt,axis=1)

plt.figure(figsize=(5,3))
plt.plot(yyyy0+np.arange(ntim)/12.,fnee_gm,'g-',label='NEE')
plt.plot(yyyy0+np.arange(ntim)/12.,foce_gm*10,'b-',label='10x OCE')
plt.plot(yyyy0+np.arange(ntim)/12.,fant_gm*3,'k-',label='3x ANT')
plt.xlim([yyyy0,yyyy1])
plt.ylabel(f"CO2 fluxes ({units['flux']})")
plt.legend()
plt.grid()
plt.tight_layout()

plt.show()
