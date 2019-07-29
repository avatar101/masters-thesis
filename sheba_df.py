import numpy as np
import pandas as pd

def sheba_df(file, dropnan=False):
    """
    To load sheba sounding data into a dataframe
    file = path + filename
    dropnan: DONT GIVE INPUT as a STRING
    Temp and Dewpt in Kelvin , pressure in hPa"""
    
    #path = '/home/ollie/muali/data_work/Sounding_data/unzipped_data/'
    df = pd.read_csv(file, delim_whitespace=True,\
                skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], header=0, dtype=float )
    
    # Quality check
    df['Press'].replace(9999.0, np.nan, inplace=True)
    df[('RH')].replace(999.0, np.nan, inplace=True)
    df[('Temp')].replace(999.0, np.nan, inplace=True)
    df[('Dewpt')].replace(999.0, np.nan, inplace=True)
    
    df['Temp'] = df['Temp'] + 273.15 # converting to K
    df['Dewpt'] = df['Dewpt'] + 273.15
    
    if dropnan == True:
        df.dropna(inplace=True)
    
    df.rename(columns={'Press': 'pressure', 'RH': 'relative_humidity', 'Temp': 'temperature', 'Dewpt': 'dewpoint'}, inplace=True)
    return df