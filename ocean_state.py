
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
from mpl_toolkits.basemap import Basemap
import numpy.ma as ma

# Setup parameters and constants
make_clim = 1
make_tran = True

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
uo   = var_file.variables['ucur'][:]
uo   = ma.masked_array(uo,mask=uo>3.9)
tim  = var_file.variables['timePlot'][:]
lev  = var_file.variables['level'][:]
lat  = var_file.variables['lat'][:]
lon  = var_file.variables['lon'][:]
var_file.close()

var_file = nc4.Dataset(data_path+'vcur.2012.nc','r')
# time/lev/lat/lon
vo = var_file.variables['vcur'][:]
vo = ma.masked_array(vo,mask=vo>3.9)
var_file.close()

var_file = nc4.Dataset(data_path+'pottmp.2012.nc','r')
# time/lev/lat/lon
theta = var_file.variables['pottmp'][:]
theta = ma.masked_array(theta,mask=theta>330)
var_file.close()


theta_am, theta_zm, theta_pp, theta_ss = comp_stat(theta)
vo_am, vo_zm, vo_pp, vo_ss = comp_stat(vo)


if make_clim is True:

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
    plt.contourf(lon,lat,np.sqrt(uo[imon,jlev,:,:]**2+vo[imon,jlev,:,:]**2),levels=np.arange(10)*0.1,cmap='Reds')
    plt.colorbar(orientation='horizontal')
    #scale_arr = 1
    #curr_map = plt.quiver(lon,lat,ucur[imon,jlev,:,:],vcur[imon,jlev,:,:],units='xy')
    #plt.quiverkey(curr_map,0.9,1.1,scale_arr,str(scale_arr))
    plt.title('Currents month= %i @ %i m' % (imon+1,lev[jlev]))


    # Lon/lat theta plot
    plt.figure()
    imon = 7 # CHANGEME (0 = Jan, 11 = Dec)
    jlev = 39 # CHANGEME (0 = 5 m, 39 = 5000 m)
    map_setup(0,360,-90,90,'none','none','none','black')
    plt.contourf(lon,lat,theta[imon,jlev,:,:],levels=270+np.arange(11)*3,cmap='bwr',extend='both')
    plt.colorbar(orientation='horizontal')
    plt.title('Theta month= %i @ %i m' % (imon+1,lev[jlev]))

    plt.show()

if make_tran is True:
   

   # Fig 13.5 PO92
   var_am = theta_am; var_pp = theta_pp; var_ss = theta_ss; var_name = 'Heat'; var_uni = 'K m/s' 

   plt.figure() 
   clevs = np.linspace(-.1,.1,11) 
   plt.contour(lat,lev,np.mean(np.mean(vo_pp*var_pp,axis=0),axis=2),levels=clevs,colors='k')
   plt.contourf(lat,lev,np.mean(np.mean(vo_pp*var_pp,axis=0),axis=2),levels=clevs,cmap='bwr')
   plt.xlim([-80,80])
   #plt.ylim([max(lev),min(lev)])
   plt.ylim([400,0])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Depth (m)')
   plt.title(var_name+' -- transient eddies ('+var_uni+')') 

   plt.figure() 
   clevs = np.linspace(-.1,.1,11)
   plt.contour(lat,lev,np.mean(np.mean(vo_ss,axis=0)*np.mean(var_ss,axis=0),axis=2),levels=clevs,colors='k')
   plt.contourf(lat,lev,np.mean(np.mean(vo_ss,axis=0)*np.mean(var_ss,axis=0),axis=2),levels=clevs,cmap='bwr')  
   plt.xlim([-80,80])
   #plt.ylim([max(lev),min(lev)])
   plt.ylim([400,0])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Depth (m)')
   plt.title(var_name+' -- stationary eddies ('+var_uni+')') 

   plt.figure() 
   clevs = np.linspace(-5,5,11)
   #plt.contour(lat,lev,np.mean(vo_am,axis=2)*np.mean(var_am,axis=2),levels=clevs,colors='k')
   #plt.contourf(lat,lev,np.mean(vo_am,axis=2)*np.mean(var_am,axis=2),levels=clevs,cmap='bwr')  
   plt.contourf(lat,lev,np.mean(vo_am,axis=2)*np.mean(var_am,axis=2),levels=clevs,cmap='bwr',extend='both')  
   plt.xlim([-80,80])
   #plt.ylim([max(lev),min(lev)])
   plt.ylim([400,0])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Depth (m)')
   plt.title(var_name+' -- mean circulation ('+var_uni+')') 

   # Layer thickness
   levp = np.append(lev[1::],lev[-1])
   dlev = levp-lev

   plt.figure()
   #plt.plot(lat,vo_am[23,:,-30]*var_am[23,:,-30])
   #plt.plot(lat,np.sum(np.mean(vo_am,axis=2)*np.mean(var_am,axis=2)*dlev[:,None],axis=0))
   plt.plot(lat,np.sum((vo_am[:,:,-33]*var_am[:,:,-33]*dlev[:,None])[0:15],axis=0))

   plt.show()
   
 




