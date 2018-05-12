import numpy as np
import pandas as pd

def sheba_df(file):
    """
    To load sheba sounding data into a dataframe
    file = filename
    """
    
    path = '/home/ollie/muali/data_work/Sounding_data/unzipped_data/'
    df = pd.read_csv(path + file, delim_whitespace=True,\
                skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15], header=0, dtype=float )
    
    # Quality check
    df['Press'].replace(9999.0, np.nan, inplace=True)
    df[('RH')].replace(999.0, np.nan, inplace=True)
    df[('Temp')].replace(999.0, np.nan, inplace=True)
    df[('Dewpt')].replace(999.0, np.nan, inplace=True)
    
    return df