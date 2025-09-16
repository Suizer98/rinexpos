# -*- coding: utf-8 -*-
"""
Julian Day Calculation
Based on MATLAB julday.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np


def julday(y, m, d, h):
    """
    Conversion of date to Julian day
    Based on MATLAB julday.m
    
    Parameters:
    -----------
    y : int
        Year (four digits)
    m : int
        Month
    d : int
        Day
    h : float or array
        Hour and fraction hereof
        
    Returns:
    --------
    jd : float or array
        Julian day number
        
    Notes:
    ------
    The conversion is only valid in the time span
    from March 1900 to February 2100
    """
    if m <= 2:
        y = y - 1
        m = m + 12
    
    jd = np.floor(365.25 * y) + np.floor(30.6001 * (m + 1)) + d + h/24 + 1720981.5
    return jd
