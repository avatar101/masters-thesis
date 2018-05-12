import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from netCDF4 import Dataset
from netCDF4 import date2index
from datetime import datetime



def traj_plot_monthly(state, month, seaice_, levels = ['780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']):
    """Function to plot monthly clear or cloudy state plots with option of monthly seaice data.
    
    Arguments: state, month, masked seaice, levels to be plotted as a list
    
    levels = ['780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600'] """
    # Extract seaice concentration value based on month
    
    # Better to ask user to give the sea ice data with proper masking
    path = 'H:/IUP/Student_job_AWI/Ollie_data/traj_sheba_sounding/winter_all/'
    
    # checking for clear or cloudy
    if (state == 'cloudy'):
        dates_ = open('C:\\Users\\Mub\\Documents\\Python_AWI\\Avg_dates\\3havg_cloudy_' + month,'r').read().split('\n')
    else:
        dates_ = open('C:\\Users\\Mub\\Documents\\Python_AWI\\Avg_dates\\3havg_clear_' + month,'r').read().split('\n')
        
    # specifying the levels or ask user to give levels as a list
    #levels = ['780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']
    
    for lvl in levels:
        #to loop over all levels
        fig = plt.figure(figsize=(12,10))
        # plt.figure(figsize=(10,8))

        m = Basemap(projection='ortho', lat_0=80, lon_0=270, resolution='l')
        m.fillcontinents(color='0.75')
        m.drawparallels(np.arange(-80.,81.,20.), color='grey')
        m.drawmeridians(np.arange(-180.,181.,20.))
        
        m.pcolormesh(lon_ice, lat_ice, seaice_, latlon=True, cmap='Blues')
        plt.clim(0, 100) # Set the color limits of the current image
        plt.colorbar(label='Sea Ice Concentration')

    # inner loop for plotting all the trajectories on one map

            # read the monthly file
        for line_ in dates_:
            df = pd.read_csv(path+'tdump_'+lvl+'_'+line_, skiprows=7, header=None, delim_whitespace=True)
            
            lat = np.array(df.iloc[:, 9].copy())
            lon = np.array(df.iloc[:, 10].copy())
    
                    #Convert lat lon to map coordinates
            x, y = m(lon, lat)
    
                    #Plot the points on the map
            plt.plot(x, y,linewidth=1.0, color='red')
        
                    #source point
            xpt, ypt = m(lon[-1], lat[-1])
            plt.plot(xpt, ypt, marker = '*', markerfacecolor='red', markersize=8)
            
        plt.title("Level: {} m AGL".format(lvl))
        plt.savefig(path1+lvl+'_'+state+month+'_test_level.png')
        plt.close(fig)


    