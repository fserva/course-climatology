
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4


# Setup parameters and constants
make_clim = True # Climatology
make_tran = False # Transport
l_e = 2.5E+6 # latent heat vaporization
rcp = 0.285 # R/Cp
cp  = 1004. # J/kg/K

# Select the background map library
map_type = 'nomap'
#map_type = 'basemap'
#map_type = 'cartopy'


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


# Compute annual and zonal means, and deviations
def comp_stat(var):
    var_am = np.mean(var,axis=0)
    var_zm = np.mean(var,axis=3)
    var_pp = var - var_am[None,:,:,:]  # prime 
    var_ss = var - var_zm[:,:,:,None]  # star
    return var_am, var_zm, var_pp, var_ss


# Open atmospheric data
data_path = './atmo_ocean_data/'
atmo_file = nc4.Dataset(data_path+'uvwtqgph_2000_01_07.nc','r')
# time/lev/lat/lon
ua   = atmo_file.variables['u'][:]
va   = atmo_file.variables['v'][:]
wa   = atmo_file.variables['w'][:]
ta   = atmo_file.variables['t'][:]
qq   = atmo_file.variables['q'][:]
zz   = atmo_file.variables['z'][:]
tim  = atmo_file.variables['time'][:]
lev  = atmo_file.variables['levelist'][:]
lat  = atmo_file.variables['latitude'][:]
lon  = atmo_file.variables['longitude'][:]
atmo_file.close()

theta  = np.zeros((len(tim),len(lev),len(lat),len(lon)),dtype='f') 
thetae = np.zeros((len(tim),len(lev),len(lat),len(lon)),dtype='f') 

# Compute potential and equivalent potential temperatures
for itim in range(len(tim)):
    for jlat in range(len(lat)):
        for klon in range(len(lon)):
            theta[itim,:,jlat,klon]  = ta[itim,:,jlat,klon]*((1000./lev)**rcp)
            thetae[itim,:,jlat,klon] = theta[itim,:,jlat,klon]*\
                                       np.exp((qq[itim,:,jlat,klon]*l_e)/\
                                               (ta[itim,:,jlat,klon]*cp))

# TODO add other vars
ta_am, ta_zm, ta_pp, ta_ss = comp_stat(ta)
va_am, va_zm, va_pp, va_ss = comp_stat(va)
theta_am, theta_zm, theta_pp, theta_ss = comp_stat(theta)
thetae_am, thetae_zm, thetae_pp, thetae_ss = comp_stat(thetae)
ta_va_am, ta_va_zm, ta_va_pp, ta_va_ss = comp_stat(ta*va)


if make_clim is True: 

    # Zonal mean plot of temperature(s)
    plt.figure()
    imon = 0 # CHANGEME (0 = Jan, 11 = Dec)
    cont_t_plot = plt.contour(lat,lev,ta_zm[imon,:,:],np.linspace(200,300,11),colors='k')
    plt.clabel(cont_t_plot,fmt='%1.0i')
    plt.contourf(lat,lev,theta_zm[imon,:,:],np.linspace(250,450,11))
    plt.yscale('log',base=10)
    plt.ylim([1000,100])
    plt.title('Temperature month= %i' % (imon+1))
    plt.colorbar()
    plt.xlabel('Latitude (deg)')
    plt.ylabel('Pressure (mb)')


    # Lon/lat wind plot
    plt.figure()
    imon = 6 # CHANGEME (0 = Jan, 11 = Dec)
    jlev = 20 # CHANGEME (0 = 1 mb, 22 = 1000 mb)
    quiv_int = 5

    if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

    if map_type == 'cartopy': # use transform keyword
        map_setup()
        plt.contourf(lon,lat,np.sqrt(ua[imon,jlev,:,:]**2+va[imon,jlev,:,:]**2),
                     levels=np.arange(10)*2,cmap='Reds',transform=ccrs.PlateCarree())
 
    if map_type in ['nomap','basemap']: # no transform
        plt.contourf(lon,lat,np.sqrt(ua[imon,jlev,:,:]**2+va[imon,jlev,:,:]**2),
                     levels=np.arange(10)*2,cmap='Reds')

    plt.colorbar(orientation='horizontal')
    scale_arr = 50
    wnd_map = plt.quiver(lon,lat,ua[imon,jlev,:,:],va[imon,jlev,:,:])#,units='xy')
    plt.quiverkey(wnd_map,X=0.9,Y=1.1,U=scale_arr,label=str(scale_arr))
    plt.title('Winds month= %i @ %i mb' % (imon+1,lev[jlev]))


    # Lon/lat temperature plot
    plt.figure()
    imon = 7 # CHANGEME (0 = Jan, 11 = Dec)
    jlev = 22 # CHANGEME (0 = 1 mb, 22 = 1000 mb)

    if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

    if map_type == 'cartopy': # use transform keyword
        map_setup()
        plt.contourf(lon,lat,ta[imon,jlev,:,:],levels=220+np.arange(11)*10,
                     cmap='bwr',extend='both',transform=ccrs.PlateCarree())

    if map_type in ['nomap','basemap']: # no transform
        plt.contourf(lon,lat,ta[imon,jlev,:,:],levels=220+np.arange(11)*10,
                     cmap='bwr',extend='both')

    plt.colorbar(orientation='horizontal')
    plt.title('Temperature month= %i @ %i mb' % (imon+1,lev[jlev]))


    # Lon/lat omega plot
    plt.figure()
    imon = 7 # CHANGEME (0 = Jan, 11 = Dec)
    jlev = 15 # CHANGEME (0 = 1 mb, 22 = 1000 mb)

    if map_type == 'basemap':
        map_setup(0,360,-90,90,'none','none','none','black')

    if map_type == 'cartopy': # use transform keyword
        map_setup()
        plt.contourf(lon,lat,wa[imon,jlev,:,:],levels=np.linspace(-0.2,0.2,11),
                     cmap='bwr',extend='both',transform=ccrs.PlateCarree())

    if map_type in ['nomap','basemap']: # no transform
        plt.contourf(lon,lat,wa[imon,jlev,:,:],levels=np.linspace(-0.2,0.2,11),
                     cmap='bwr',extend='both')

    plt.colorbar(orientation='horizontal')
    plt.title('Pressure tendency month= %i @ %i mb' % (imon+1,lev[jlev]))


    # Temperature(s) profiles
    plt.figure()
    imon = 0 # CHANGEME (0 = Jan, 11 = Dec)
    jlat = 36 # CHANGEME (0 = 90N, 72 = 90S)
    plt.plot(ta_zm[imon,:,jlat],lev,'k-',label='temp')
    plt.plot(theta_zm[imon,:,jlat],lev,'k--',label='theta')
    plt.yscale('log',base=10)
    plt.ylim([1000,100])
    plt.xlim([200,400])
    plt.legend()
    plt.xlabel('T (K)')
    plt.ylabel('Pressure (mb)')
    plt.title('Temperature month= %i @ lat= %i' % (imon+1,lat[jlat]))

    plt.figure()
    imon = 0 # CHANGEME (0 = Jan, 11 = Dec)
    jlat = 25 # CHANGEME (0 = 90N, 72 = 90S)
    plt.plot(theta_zm[imon,:,jlat],lev,'k-',label='theta')
    plt.plot(thetae_zm[imon,:,jlat],lev,'k--',label='thetae')
    plt.yscale('log',base=10)
    plt.ylim([1000,100])
    plt.xlim([250,350])
    plt.legend()
    plt.xlabel('T (K)')
    plt.ylabel('Pressure (mb)')
    plt.title('Potential temperature month= %i @ lat= %i' % (imon+1,lat[jlat]))



if make_tran is True: 

   # Fig 13.5 PO92
   var_am = ta_am; var_pp = ta_pp; var_ss = ta_ss; var_name = 'Sensible heat'; var_uni = 'K m/s' 

   plt.figure() 
   clevs = np.linspace(-10,10,11) 
   plt.contour(lat,lev,np.mean(np.mean(va_pp*var_pp,axis=0),axis=2),levels=clevs,colors='k')
   plt.contourf(lat,lev,np.mean(np.mean(va_pp*var_pp,axis=0),axis=2),levels=clevs,cmap='bwr')
   plt.xlim([-80,80])
   plt.ylim([1000,150])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Pressure (mb)')
   plt.title(var_name+' -- transient eddies ('+var_uni+')') 

   plt.figure() 
   clevs = np.linspace(-5,5,11)
   plt.contour(lat,lev,np.mean(np.mean(va_ss,axis=0)*np.mean(var_ss,axis=0),axis=2),levels=clevs,colors='k')
   plt.contourf(lat,lev,np.mean(np.mean(va_ss,axis=0)*np.mean(var_ss,axis=0),axis=2),levels=clevs,cmap='bwr')  
   plt.xlim([-80,80])
   plt.ylim([1000,150])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Pressure (mb)')
   plt.title(var_name+' -- stationary eddies ('+var_uni+')') 

   plt.figure() 
   clevs = np.linspace(-500,500,11)
   plt.contour(lat,lev,np.mean(va_am,axis=2)*np.mean(var_am,axis=2),levels=clevs,colors='k')
   plt.contourf(lat,lev,np.mean(va_am,axis=2)*np.mean(var_am,axis=2),levels=clevs,cmap='bwr')  
   plt.xlim([-80,80])
   plt.ylim([1000,150])
   plt.colorbar(orientation='horizontal')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Pressure (mb)')
   plt.title(var_name+' -- mean circulation ('+var_uni+')') 

   # Annual mean time series (TODO add weighting)
   levt = lev[12:23] # 200-1000 hPa
   ts_tran = np.mean(np.mean(np.mean(va_pp*var_pp,axis=0),axis=2)[12:23,:],axis=0)
   ts_stat = np.mean(np.mean(np.mean(va_ss,axis=0)*np.mean(var_ss,axis=0),axis=2)[12:23,:],axis=0)
   ts_mean = np.mean(np.mean(va_am,axis=2)[12:23,:]*np.mean(var_am,axis=2)[12:23,:],axis=0)

   plt.figure()
   plt.plot(lat,ts_tran*10,'k-',label='10x trans')
   plt.plot(lat,ts_stat*10,'k--',label='10x stat')
   plt.plot(lat,ts_mean,'k:',label='mean')
   plt.xlim([-60,60])  
   plt.ylim([-40,40])  
   plt.axhline(0,color='grey')
   plt.xlabel('Latitude (deg)')
   plt.ylabel('Northward flux ('+var_uni+')')
   plt.legend()
   plt.show()



plt.show()
