
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
from mpl_toolkits.basemap import Basemap

# Setup parameters and constants
#make_ocean = False  # Oceanic analysis
rcp = 0.285 # R/Cp

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


# Compute annual and zonal means, and deviations
def comp_stat(var):
    var_am = np.mean(var,axis=0)
    var_zm = np.mean(var,axis=3)
    var_pp = var - var_am[None,:,:,:]  # prime 
    var_ss = var - var_zm[:,:,:,None]  # star
    return var_am, var_zm, var_pp, var_ss


# Open oceanic data
data_path = './atmo_ocean_data/'
var_file = nc4.Dataset(data_path+'ucur.2012.nc','r')
# time/lev/lat/lon
ucur   = var_file.variables['ucur'][:]
tim  = var_file.variables['timePlot'][:]
lev  = var_file.variables['level'][:]
lat  = var_file.variables['lat'][:]
lon  = var_file.variables['lon'][:]
var_file.close()

var_file = nc4.Dataset(data_path+'vcur.2012.nc','r')
# time/lev/lat/lon
vcur   = var_file.variables['vcur'][:]
var_file.close()

var_file = nc4.Dataset(data_path+'pottmp.2012.nc','r')
# time/lev/lat/lon
theta   = var_file.variables['pottmp'][:]
var_file.close()


theta_am, theta_zm, theta_pp, theta_ss = comp_stat(theta)

# Zonal mean plot of temperature(s)
plt.figure()
imon = 0 # CHANGEME (0 = Jan, 11 = Dec)
#cont_t_plot = plt.contour(lat,lev,ta_zm[imon,:,:],np.linspace(200,300,11),colors='k')
#plt.clabel(cont_t_plot,fmt='%1.0i')
plt.contourf(lat,lev,theta_zm[imon,:,:],np.linspace(260,300,11))
plt.ylim([max(lev),min(lev)])
plt.title('Temperature month= %i' % (imon+1))
plt.colorbar()
plt.xlabel('Latitude (deg)')
plt.ylabel('Depth (m)')


# Lon/lat currents plot
plt.figure()
imon = 7 # CHANGEME (0 = Jan, 11 = Dec)
jlev = 10 # CHANGEME (0 = 5 m, 39 = 5000 m)
quiv_int = 5
map_setup(0,360,-90,90,'none','none','none','black')
plt.contourf(lon,lat,np.sqrt(ucur[imon,jlev,:,:]**2+vcur[imon,jlev,:,:]**2),levels=np.arange(10)*0.1,cmap='Reds')
plt.colorbar(orientation='horizontal')
#scale_arr = 1
#curr_map = plt.quiver(lon,lat,ucur[imon,jlev,:,:],vcur[imon,jlev,:,:],units='xy')
#plt.quiverkey(curr_map,0.9,1.1,scale_arr,str(scale_arr))
plt.title('Currents month= %i @ %i m' % (imon+1,lev[jlev]))


# Lon/lat theta plot
plt.figure()
imon = 7 # CHANGEME (0 = Jan, 11 = Dec)
jlev = 10 # CHANGEME (0 = 5 m, 39 = 5000 m)
map_setup(0,360,-90,90,'none','none','none','black')
plt.contourf(lon,lat,theta[imon,jlev,:,:],levels=270+np.arange(11)*3,cmap='bwr',extend='both')
plt.colorbar(orientation='horizontal')
plt.title('Theta month= %i @ %i m' % (imon+1,lev[jlev]))


plt.show()

