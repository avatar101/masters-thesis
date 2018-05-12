import numpy as np
class sounding_df:
    
    def __init__(self, df):
        # this __init__ method is used to create new objects inside the class
        self.p = np.array(df['Pressure'])
        self.temp = np.array(df['Temp'])
        self.dew = np.array(df['Dewpt'])
        
    def spec_humidity(self, latent='water'):
        """Calculates SH automatically from the dewpt. Returns in g/kg"""
        # Declaring constants
        self.e0 = 6.113 # saturation vapor pressure in hPa
        # e0 and Pressure have to be in same units
        self.c_water = 5423 # L/R for water in K
        self.c_ice = 6139 # L/R for ice in K
        self.T0 = 273.15 # Kelvin
        
        if latent == 'water' or latent == 'Water':
            self.c = self.c_water    # using c for water
        
        else:
            self.c= self.c_ice       # using c_ice for ice, clear state
     
        sat_vapor = self.e0 * np.exp((self.c * (self.temp -self.T0))/(self.temp * self.T0)) #hPa becuase of e0
 
        self.q = (622 * self.e0 * np.exp(self.c * (self.dew - self.T0)/(self.dew * self.T0)))/self.p # g/kg 
        # 622 is the ratio of Rd/Rv in g/kg
        return self.q