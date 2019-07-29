import numpy as np
import pandas as pd
from geopy.distance import geodesic
from dateutil.parser import parse

def trajcheck(file, lat_diff=1., lon_diff=1., search=None, path = '/home/ollie/muali/Data/winter_all/'):
    """This function checks if a given trajectory is passing through a observation station.
    Outputs the matching hour, Obs Station Name, etc.
    Modified to give distance in km between the traj and station as well
    
    file_= Name of the time from winter_all folder as'tdump_lvl_MM_DD_HH'
    
    lat_diff= Minimum latitude difference to satisfy, default 1.0
    
    lon_diff =Minimum latitude difference to satisfy, default 1.0
    
    search: (str) to be used for searching a pattern from the output
    
    path: default is winter_all folder """
    
    
    
    
    file_name = path + file
    
    df_IGR = pd.read_excel('/home/ollie/muali/python_notebooks/IGR_25N_v2.xlsx')
    #f = open(file_name,'rb+')
    
    # getting launch date
    #for i, file_ in enumerate(f):
     #   if i ==4: # reads 6th line
      #      date_str = f.read(25)
       #     f.close()
    #l_date = parse(date_str)
    
    df = pd.read_csv(file_name, skiprows=7, header=None, delim_whitespace=True) 
    # a very efficient way to rename columns
    # dict to rename columns
    cols_renames = {2: 'year', 3: 'month', 4: 'day', 5: 'hour', 6: 'minute'}

    # converting year to 4 digits
    df.iloc[:,2] = df.iloc[:,2] + 1900

    # df_subset is used to merge yy, mm, dd, hh values into BT_time column
    df_subset = df.loc[:, list(cols_renames.keys())].rename(columns=cols_renames)
    # df_subset is extracting the time from the original dataframe to be used to make a time index for the final dataframe
    dt_series = pd.to_datetime(df_subset) # converts the df into a time series which we will add as extra column
    dt_series.head()
    # adding a new backtrajectory column
    df['BT_time'] = dt_series # adding the back trajectory time column to df
    
    # dropping the not required columns
    df.drop([0,1,2,3,4,5,6,7], axis =1, inplace=True)
    df.head()
    
    col_rename2 = {8: 'back_hr', 9:'Lat', 10: 'Lon', 11:'AGL', 12:'Pressure'}
    df.rename(columns=col_rename2, inplace=True)

    del df_subset
    del dt_series
    
    count = 0
    # count will be used to tell how many times our condition is met
    
    string_list =[] # to store the output of print to be used by regex
    for row_IRG in df_IGR.itertuples():
        for row in df.itertuples():
            # lat_diff lon_diff provided by the user
            if ((-lat_diff < (row_IRG.Lat - row.Lat) < lat_diff) & (-lon_diff < (row_IRG.Lon - row.Lon) < lon_diff)):
              #  print(row.back_hr, row.BT_time, row_IRG.ID, row_IRG.Lat, row_IRG.Lon ,row_IRG.Lat - row.Lat, row_IRG.Lon - row.Lon)
#                print(row.back_hr, row.BT_time.strftime('%d-%m-%Y %H:%M'), row_IRG.ID, row_IRG.Lat, row_IRG.Lon , row.Lat - row_IRG.Lat, row.Lon - row_IRG.Lon, geodesic((row.Lat, row.Lon), (row_IRG.Lat, row_IRG.Lon)).km )
                string_list.append((row.back_hr, row.BT_time.strftime('%d-%m-%Y %H:%M'), row_IRG.ID, row_IRG.Lat, row_IRG.Lon , row.Lat - row_IRG.Lat, row.Lon - row_IRG.Lon, geodesic((row.Lat, row.Lon), (row_IRG.Lat, row_IRG.Lon)).km ))
                count = count + 1
    
    print("The following are the counts:")
    print(count)
    
    if search is not None:
        for item in string_list:
            if search in item:
                print(item,'\n')
                
    else:
        for item in string_list:
            print(item,'\n')
# eof