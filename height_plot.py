import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
import seaborn as sns
from netCDF4 import Dataset
from netCDF4 import date2index
from datetime import datetime

def height_plot(*dates, path, path_save=None, plot_name='height_plot', save_fig=None, size=(14,8), pixel=100, rows=7, levels = ['400', '780', '1000', '1400', '1850', '2850']):
    """Function to plot heights for trajectories for variable dates for user specified levels on a single plot.
    
    Input arguments: 
    date: as a datetime.datetime object Eg, datetime(1997,12,1,23)
    path: path of data file to be plotted
    path2: path where the file is desired to be saved
    
    save_fig: Default doesn't save
    size: controls figure size. To be given as tuple
    pixel: Alter dpi for resolution
    rows: No of rows to skip while reading the trajectory data. Default 7 but depends on number of Meteo files used while traj 
    calculation
   
    levels: to plot as a list of strings
    Eg, levels = ['400', '780', '1000', '1400', '1850', '2850', '3950', '5220', '6730', '8600']
    """
    
    #print(date_str) 
    date_str = ['{:%m_%d_%H}'.format(date) for date in dates]
    
    fig, ax = plt.subplots(figsize=size, dpi=pixel)
     
        
    #path = '/home/ollie/muali/Data/winter_all/'
    
    #file_name = [path + file for file in file]
    #print (file_name)
    #for f in file_name:
    #ax2 = ax.twinx() # to make an axis on right
    
    for d_ in date_str:
        for lvl in levels:
            df = pd.read_csv(path+'tdump_'+lvl+'_'+d_, skiprows=rows, header=None, delim_whitespace=True)
           # df = pd.read_csv(f, skiprows=7, header=None, delim_whitespace=True) 
            # a very efficient way to rename columns
            # dict to rename columns
            cols_renames = {2: 'year', 3: 'month', 4: 'day', 5: 'hour', 6: 'minute'}

            # converting year to 4 digits
            df.iloc[:,2] = df.iloc[:,2] + 1900

            # df_subset is used to merge yy, mm, dd, hh values into BT_time column
            df_subset = df.loc[:, list(cols_renames.keys())].rename(columns=cols_renames)
            dt_series = pd.to_datetime(df_subset)
            dt_series.head()
            # adding a new backtrajectory column
            df['BT_time'] = dt_series

            # dropping the not required columns
            df.drop([0,1,2,3,4,5,6,7], axis =1, inplace=True)
            df.head()

            col_rename2 = {8: 'back_hr', 9:'Lat', 10: 'Lon', 11:'AGL', 12:'Pressure'}
            df.rename(columns=col_rename2, inplace=True)

            #plotting

            ax.plot(df['back_hr'], df['AGL'], label = lvl+' m')
            #ax2.plot(df['back_hr'], df['Pressure'], label = lvl+'m')
           # ax2.set_yticks(df['Pressure'].values)
            # height and pressure are not varying similarly in the atmosphere
            # hence the curves won't be same
            ax.set_xticks(df['back_hr'].values[::10]); # axis can be controlled at every 6 hours
            
            
            ax.legend()
            ax.set_ylabel('Height above ground (m)')
            ax.set_xlabel('Hours from SHEBA')
            del df_subset
            del dt_series
    all_dates = "" # to print dates in the title
    for date in dates:
        all_dates +='{}'.format(date)+" "
        
    ax.set_title('Evolution of Trajectories for ' +all_dates)       
    sns.despine(offset=10)
    sns.set_style("ticks") 
    
    if save_fig != None:
        # saving fig #saves at path2
        plt.savefig(path2 + plot_name + '.png')
        plt.close(fig)
    else:
        plt.show(fig)