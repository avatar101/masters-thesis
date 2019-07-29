import numpy as np
import metpy.calc as mcalc
from metpy.units import units

class sounding_df:
    """Class containing definitions of specific humidity,  
    RH with respect to water, RH wrt ice and Total Precipitable water. 
    Create a class object by giving it a sounding data as 
    Pandas dataframe.
    Author: Syed Mubashshir Ali
    """
    
    def __init__(self, df):
        # __init__ method is used to create new objects inside the class
        
        # Symbols used
        # p = pressure
        # T = Temperature
        # dew = dew point temperature
        # esw = saturation vapor pressure with respect to a flat surface of water in hPa
        # esi = saturation vapor pressure with respect to a flat surface of ice in hPa
        # L = Lv = Latent heat of vaporization of liquid water = 2.5x10^6 J/Kg
        # Ld = Latent heat of deposition for ice = 2.83X10^6 J/Kg
        # Rv = water-vapor gas constant = 461 J/K/Kg
        # Rd = gas constant for dry air
        # e0 = saturated vapor pressure at 273K = 6.13 hPa # not required
        self.p = np.array(df['pressure']) #hPa
        self.T = np.array(df['temperature']) # in Kelvin
        self.dew = np.array(df['dewpoint']) # in Kelvin
        self.esw = 6.113 
        self.esi = 6.107 
        # e0 and Pressure have to be in same units
        self.cw = 5423 # L/Rv for water, units in Kelvin
        self.ci = 6139 # Ld/Rv for ice, units in Kelvin
        self.T0 = 273.15 # Kelvin
        
    def spec_humidity(self, latent='water'):
        """Calculates SH automatically from the dewpt. Returns in g/kg"""
        # Declaring constants

        
        if latent == 'water' or latent == 'Water':
            self.c = self.cw    # using c for water
        
        else:
            self.c= self.ci       # specific humidity with respect to ice
        
                
        #calculating specific humidity, q directly from dew point temperature
        #using equation 4.24, Pg 96 Practical Meteorolgy (Roland Stull)
        self.q = (622 * self.esw * np.exp(self.c * (self.dew - self.T0)/(self.dew * self.T0)))/self.p # g/kg 
        # 622 is the ratio of Rd/Rv in g/kg

        return self.q
    
    def relative_humidity(self):
        """Calculates RH with respect to flat surface of water"""
        # Uses the definition of RH = vapor pressure/ saturation vapor pressure
        # the vapor pressure and saturation vapor pressure are calculated by using Clasius Clapeyron equation
        # Refer Practical Meteorology (Roland Stull) Pg 88, 89
        # Equation below is derived on algebraic simplification without any approximation
        
        self.RH_w = 100* np.exp(self.cw * (self.dew - self.T)/(self.T * self.dew))
        self.RH_w [self.RH_w > 120.] = 120 # assign RH = 100 for supersaturated values.
        return self.RH_w
    
    def relative_humidity_ice(self):
        
        """Calculates RH with respect to ice"""
        
        self.RH_i = 100* (self.esw/self.esi) * np.exp( ( (5423/self.T0 - 6139/self.T0) - 5423/self.dew + 6139/ self.T) )
        
        return self.RH_i
    
    def tpw(self, top=None):
        """ Calculates total precipitable water taking only water vapors into the account"""
        
        if top is None:
            top = np.min(self.p)*units.hectopascal + .01 * units.hPa
            
        self.total_pw = mcalc.precipitable_water(dewpt=self.dew *units.K, pressure=self.p *units.hectopascal, top=top) 
        # has a padding factor to avoid error due to float point comparision
        
        return self.total_pw
    def potential_t(self):
        "Calculates potential temperature for the given profile using metpy function"
        
        self.pot_t = mcalc.potential_temperature(self.p * units.hectopascal, self.T * units.kelvin)
        
        return self.pot_t