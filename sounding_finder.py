import os
import pandas as pd
import numpy as np
#from io import StringIO
from collections import deque
from itertools import takewhile


def sounding_finder(file ,from_line, to_line, derived=False, to_print=None, to_df=None ):
    """ To read IGRA data-set
    Arguments:
    
    file: ID of the station name only. Eg, 'RSM00022271'
    from_line: Line to match as a string. Eg, '#RSM00022271 1997 12 30'
    to_line: Line up to match as a string. Eg, '#RSM00022271 1997 12 30 12'
    to_print: Use it to print the matched dates in the file
    to_df: To save the extracted value as a dataframe with variable df.
    
    When to_df is not None, the function returns a df
    
    Also returns p_+file, temp_+file, dew_+file as np arrays
    
    """
    global df
    
    if derived is True:
    # To read IGRA derived files
    
    
        path = '/home/ollie/muali/Data/'

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

        
        df = None

        if to_df != None:

            col = [(1,7), (17,23), (25,31), (33,39), (41,47), (49,55), (57,63), (65,71), (73-79), (81,87), (89,95), (97,103), (105,111), (113,119), (121,127), (129,135), (137,143), (145,151)]
            col_names = ['Pressure', 'Gph', 'Temp', 'Temp Grad', 'Pot T', 'Pot T Grad', 'Virt T', 'VPot T', 'Vap Pressure',\
                         'Sat VPressure', 'RH', 'RH Cal', 'RH Grad', 'Uwind', 'U W Grad', 'Vwind', 'V W Grad', 'Refractive I']
            df = pd.read_fwf('copyIGRA.txt', header=None, colspecs= col, names=col_names, na_values=['-9999.0'])



            df[['Temp', 'Temp Grad', 'Pot T', 'Pot T Grad', 'Virt T', 'VPot T',  'RH', 'RH Cal', 'RH Grad', 'Uwind', 'U W Grad', 'Vwind', 'V W Grad']] = df[['Temp', 'Temp Grad', 'Pot T', 'Pot T Grad', 'Virt T', 'VPot T',  'RH', 'RH Cal', 'RH Grad', 'Uwind', 'U W Grad', 'Vwind', 'V W Grad']]/10 # dividing them by 10, see read me

            df['Pressure', 'Vap Pressure', 'Sat VPressure'] = df['Pressure', 'Vap Pressure', 'Sat VPressure']/100 # converting to hPa or millibar

            df = df.dropna(subset=('Pressure', 'Temp'), how='any').reset_index(drop=True) # dropping nan


        os.remove('copyIGRA.txt') # delete opened file to free up memory

    
    else:
        

        path = '/home/ollie/muali/Data/IGRA_unzipped/'

        f2 = open('copyIGRA.txt','w')

        with open(path+file+'-data.txt','r') as f1:
            lines = (line.strip() for line in f1) # removing trailing '\n'

            # fast-forward up to from_line
            deque(takewhile(lambda x: x[0:len(from_line)] != from_line, lines), maxlen=0)

            for line in takewhile(lambda x: x[0:len(to_line)] !=to_line, lines):
                f2.write(line)
                f2.write('\n')
                if to_print != None:
                    print(line)

         # where i use itertools.takewhile to get an iterator over the lines until a contition is met (until the first header is found in your case).

         #the deque part is just the consume pattern suggested in the itertools recipes. it just fast-forwards to the point where the given condition does not hold anymore. 

        f2.close()

       
        df = None   # if user doesn't want df, the function return none

        if to_df != None:

            col = [(0,2), (3,8), (9,15), (16,21), (22,27), (28,33), (34,39), (40,45), (46,51)]
            col_names = ['Ltyp', 'Etime', 'pressure', 'Gph', 'temperature',\
                        'relative_humidity' , 'dewpoint', 'Wdir', 'Wspd']
            df = pd.read_fwf('copyIGRA.txt', header=None, colspecs= col, names=col_names, na_values=('-8888','-9999'))

            #df[['pressure','temperature', 'ewpt', 'Wspd']] = df[['Pressure','Temp', 'Dewpt', 'Wspd']].replace(-9999, np.nan)
            #df[['Temp', 'Dewpt', 'Wspd']] = df[['Temp', 'Dewpt', 'Wspd']].replace(-8888, np.nan)# means missing values
            #df.replace(-8888, np.nan, inplace=True) # 8888 means value removed by quality check

            df[['temperature', 'relative_humidity', 'dewpoint', 'Wspd']] = df[['temperature', 'relative_humidity', 'dewpoint',\
            'Wspd']]/10 # dividing them by 10, see read me
            df['temperature'] = df['temperature'] + 273.15  # to change in Kelvin
            df['dewpoint'] = df['temperature'] - df['dewpoint'] # converting Dewpt depression to Dewpt
            df['pressure'] = df['pressure']/100 # converting to hPa or millibar

            df = df.dropna(subset=('pressure', 'temperature', 'dewpoint'), how='any').reset_index(drop=True) # dropping nan

            #global p_+file, temp_+file, dew_+file

            #p_+file = np.array(df['Pressure'])
            #temp_+file = np.array(df['Temp'])
            #dew_+file= np.array(df['Dewpt'])

        os.remove('copyIGRA.txt') # delete opened file to free up memory


    
    return df

