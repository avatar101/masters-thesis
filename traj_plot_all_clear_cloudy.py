import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from netCDF4 import Dataset
from netCDF4 import date2index
from datetime import datetime


def traj_plot_all_clear_cloudy(*months, path, state, levels = ['780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']):
    """
    Function to plot trajectories of all clear or cloudy states or according to month
    path: path to data file to be plotted
    state: clear or cloudy
    """

    
    # specifying the levels or ask user to give levels as a list
    #levels = ['780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']
    fig = plt.figure(figsize=(12,10))
        # plt.figure(figsize=(10,8))

    m = Basemap(projection='ortho', lat_0=80, lon_0=270, resolution='l')
    m.fillcontinents(color='0.75')
    m.drawparallels(np.arange(-80.,81.,20.), color='grey')
    m.drawmeridians(np.arange(-180.,181.,20.))
    
    mons = [mo for mo in months]
    
    dates_=[]
       
    # checking for clear or cloudy
    if (state == 'cloudy'):
        for mo in mons:
            # makes a list of list
            # each month dates are stored as a separate list with dates as strings
            dates_.append(open('/home/ollie/muali/python_notebooks/Avg_dates/3havg_cloudy_'+ mo,'r').read().split('\n'))
    else:
        for mo in mons:
            dates_ = open('/home/ollie/muali/python_notebooks/Avg_dates/3havg_clear_'+ mo,'r').read().split('\n')
        
       
    for lvl in levels:
        #to loop over all levels
        # inner loop for plotting all the trajectories on one map

        # read the trajectories to be plotted
        for line_ in dates_:
            # element by element reading the dates
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
            
        #plt.title("Level: {} m AGL".format(lvl))
        #plt.savefig(path1+lvl+'_'+state+month+'_test_level.png')
        #plt.close(fig)

