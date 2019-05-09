
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



def map_setup(lon1,lon2,lat1,lat2,col_con,col_lake,col_sea,col_bound):
    mymap = Basemap(projection='cyl',llcrnrlon=lon1, urcrnrlon=lon2, \
            llcrnrlat=lat1, urcrnrlat=lat2, \
            lon_0=0, lat_0=0, resolution='c')

    mymap.fillcontinents(color=col_con,lake_color=col_lake)
    mymap.drawmapboundary(fill_color=col_sea)
    mymap.drawcoastlines(color=col_bound,linewidth=.35)

    mymap.drawmeridians(np.arange(0,360,30),color='gray',linewidth=.25)
    mymap.drawparallels(np.arange(-90,90,30),color='gray',linewidth=.25)

    return mymap
#

plt.figure()

map_setup(0,360,-90,90,'none','none','none','dimgray')

plt.show()
