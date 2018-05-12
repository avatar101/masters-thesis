import numpy as np

def spec_humidity(pressure, temp, temp_d, rh=None, latent='water'):
    """"
    Write Docum"""

    e0 = 6.113 # saturation vapor pressure in hPa
    c_water = 5423 # L/R for water in K
    c_ice = 6139 # L/R for ice in K
    T0 = 273.15 # Kelvin

    if latent == 'water' or latent == 'Water':
        c = c_water    # using c for water
        
    else:
        c= c_ice       # using c_ice for ice, clear state
     
    sat_vapor = e0 * np.exp((c * (temp -T0))/(temp * T0)) 
 
    
    if rh != None:
        
        # calculating it from RH
        vapor_press = rh * sat_vapor
        q = (622 * vapor_press)/(pressure - vapor_press * (1.000-622)) # specific humidity (g/kg)
        
    else:
     #   vapor_press = e0 * np.exp((c * (T_dew - T0))/(T_dew * T0))
        
    # calculating specific humidity from dept temp
    
        q = (622 * e0 * np.exp(c * (temp_d - T0)/(temp_d * T0)))/pressure # g/kg 
    
    return q