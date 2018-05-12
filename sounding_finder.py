import os
import pandas as pd
import numpy as np
#from io import StringIO
from collections import deque
from itertools import takewhile


def sounding_finder(file, from_line, to_line, to_print=None, to_df=None ):
    """
    Arguments:
    
    file: ID of the station name only. Eg, 'RSM00022271'
    from_line: Line to match as a string. Eg, '#RSM00022271 1997 12 30'
    to_line: Line up to match as a string. Eg, '#RSM00022271 1997 12 30 12'
    to_print: To be used when the matched file is required to print
    to_df: To save the extracted value as a dataframe with variable df.
    
    When to_df is not None, the function returns a df
    
    """
    path = '/home/ollie/muali/Data/IGRA_unzipped/'
    
    f2 = open('copyIGRA.txt','w')
    
    with open(path+file+'-data.txt','r') as f1:
        lines = (line.strip() for line in f1)

        deque(takewhile(lambda x: x[0:len(from_line)] != from_line, lines), maxlen=0)

        for line in takewhile(lambda x: x[0:len(to_line)] !=to_line, lines):
            f2.write(line)
            f2.write('\n')
            if to_print != None:
                print(line)
            
    f2.close()
    
    global df
    df = None   # if user doesn't want df, the function return none
    
    if to_df != None:
        
        col = [(0,2), (3,8), (9,15), (15,16), (16,21), (21,22), (22,27), (27,28), (28,33), (34,39), (40,45), (46,51)]
        col_names = ['Ltyp', 'Etime', 'Pressure', 'Pflag', 'Gph', 'Gflag', 'Temp', 'Tflag',\
                    'RH' , 'Dewpt', 'Wdir', 'Wspd']
        df = pd.read_fwf('copyIGRA.txt', header=None, colspecs= col, names=col_names)
        df.replace(-9999, np.nan , inplace=True)
        df[['Temp', 'RH', 'Wspd']] = df[['Temp', 'RH', 'Wspd']]/10 
        df['Temp'] = df['Temp'] + 273.15  # to change in Kelvin
    
    os.remove('copyIGRA.txt')
    return df