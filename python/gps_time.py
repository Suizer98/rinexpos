# -*- coding: utf-8 -*-
"""
GPS Time Calculation
Based on MATLAB gps_time.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np


def gps_time(julday):
    """
    Conversion of Julian Day number to GPS week and seconds of week
    Based on MATLAB gps_time.m
    
    Parameters:
    -----------
    julday : float or array
        Julian day number
        
    Returns:
    --------
    week : float or array
        GPS week number
    sec_of_week : float or array
        Seconds of week reckoned from Saturday midnight
    """
    a = np.floor(julday + 0.5)
    b = a + 1537
    c = np.floor((b - 122.1) / 365.25)
    e = np.floor(365.25 * c)
    f = np.floor((b - e) / 30.6001)
    d = b - e - np.floor(30.6001 * f) + np.mod(julday + 0.5, 1)
    day_of_week = np.mod(np.floor(julday + 0.5), 7)
    week = np.floor((julday - 2444244.5) / 7)
    
    # GPS week starts at Saturday midnight (day_of_week = 6)
    # Adjust day_of_week so that Saturday = 0
    day_of_week = (day_of_week + 1) % 7
    sec_of_week = (np.mod(d, 1) + day_of_week) * 86400
    
    # Handle array comparison properly - use np.where for element-wise condition
    sec_of_week = np.where(sec_of_week >= 604800.0, sec_of_week - 604800.0, sec_of_week)
    
    return week, sec_of_week
