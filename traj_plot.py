import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from netCDF4 import Dataset
from netCDF4 import date2index
from datetime import datetime


def traj_plot(*dates, path, path_save=None, plot_name='traj_plot', sea_ice='Yes', save_fig=None, size=(12,10), pixel=None, rows=7, levels = ['400', '780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']):
    
    """Function to plot trajectories for a variable dates for user specified levels with an option for sea_ice
    brackground on a single plot.
    
    Input arguments: 
    date: as a datetime.datetime object Eg, datetime(1997,12,1,23)
    path: path of data file to be plotted
    path_save: Default none, path where the file is desired to be saved
    sea_ice: 'Yes' or 'Y' to plot sea_ice
    save_fig: Default doesn't save
    size: controls figure size. To be given as tuple
    pixel: Alter dpi for resolution
    rows: No of rows to skip while reading the trajectory data. Default 7 but depends on number of Meteo files used while traj 
    calculation
   
    levels: to plot as a list of strings
    Eg, levels = ['400', '780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600'] """
    
    # path
    
    date_str = ['{:%m_%d_%H}'.format(date) for date in dates]
    #print(date_str) 
    
    # creating a basemap
    fig = plt.figure(figsize=size, dpi=pixel)
        # plt.figure(figsize=(10,8))
        
    m = Basemap(projection='ortho', lat_0=80, lon_0=270, resolution='l')
    m.fillcontinents(color='0.75')
    m.drawparallels(np.arange(-80.,81.,20.), color='grey')
    m.drawmeridians(np.arange(-180.,181.,20.))
    
    if (sea_ice == 'Yes' or sea_ice == 'Y'):    
        # Reading Sea Ice data
        filename_ = 'h://IUP/Student_job_AWI/HySplit/data/G10010_SeaIce/G10010_SIBT1850_v1.1.nc'
        # for ollie use this path
        #filename_ = '/home/ollie/muali/Data/G10010_SeaIce/G10010_SIBT1850_v1.1.nc'
        ds = Dataset(filename_)
        
        # to get the time index out of the netcdf variable
        # change it according to the month you want to plot
        # Eg, dec here
        # timeindex gives you the index of in the netcdf file
        
        timeindex = date2index(datetime(dates[0].year,dates[0].month,15),ds.variables['time'])
        lats_ice = ds.variables['latitude'][:]
        lons_ice = ds.variables['longitude'][:]
    
        #note that lon goes from 0 to 360
        # should we do a -180 here? No, basemap adjusts it automatically
        # creating our meshgrid according to data coordinates given

        lon_ice, lat_ice = np.meshgrid(lons_ice, lats_ice)
        # meshgrid creates a coordinate system with our axis supplied

        # getting seaice for SHEBA december as an eg but it works for all months
        sea_ice_dec = ds.variables['seaice_conc'][timeindex,:,:] # month dependent on user date
        # masking the low seaice concentration value
        # check low sea ice value by np.sea_ice_dec.mina
        # masking since min sea Ice is -1 for continents
        sea_ice_dec = np.ma.masked_where(sea_ice_dec<=0,sea_ice_dec) 
        ds.close()
        
        # plotting Sea Ice
        m.pcolormesh(lon_ice, lat_ice, sea_ice_dec, latlon=True, cmap='Blues')
        plt.clim(0, 100) # Set the color limits of the current image
        plt.colorbar(label='Sea Ice Concentration')
    
    
    all_dates = "" # to print dates in the title
    
    for d_ in date_str:
       # print("\n", d_)
        for lvl in levels:
            df = pd.read_csv(path+'tdump_'+lvl+'_'+d_, skiprows=rows, header=None, delim_whitespace=True)
        
        #taking lat lons of the trajectories to be plotted
            lat = np.array(df.iloc[:, 9].copy())
            lon = np.array(df.iloc[:, 10].copy())
    
        #Convert lat lon to map coordinates
            x, y = m(lon, lat)
    
        #Plot the points on the map
            plt.plot(x, y,linewidth=1.0, color='red')
        
        #source point
            xpt, ypt = m(lon[-1], lat[-1])
            plt.plot(xpt, ypt, marker = '*', markerfacecolor='red', markersize=4)
            # Text
            plt.text(xpt,ypt,lvl, fontsize=8, color='red')
           # plt.text(xpt,ypt,'Source (%5.1fW,%3.1fN)' % (lonpt,latpt), color='yellow', fontsize=15)
            
    for date in dates:
        all_dates +='{}'.format(date)+" "
            
    plt.title(all_dates)
    if save_fig != None:
        # saving fig
        plt.savefig(path2 + plot_name + '.png')
        plt.close(fig)
    else:
        plt.show(fig)