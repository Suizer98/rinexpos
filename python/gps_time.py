# -*- coding: utf-8 -*-
"""
GPS Time Calculation
Based on MATLAB gps_time.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np
from datetime import datetime, timedelta


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


def gps_time_to_datetime_iso(gps_seconds, year, month, day):
    """
    Convert GPS seconds of week to ISO format datetime
    
    Parameters:
    -----------
    gps_seconds : float
        GPS seconds of week
    year : int
        Year
    month : int
        Day
        
    Returns:
    --------
    datetime_str : str
        ISO formatted datetime string (YYYY-MM-DDTHH:MM:SSZ)
    """
    # GPS epoch: January 6, 1980 00:00:00 UTC
    gps_epoch = datetime(1980, 1, 6)
    
    # Calculate the number of weeks since GPS epoch
    current_date = datetime(year, month, day)
    days_since_epoch = (current_date - gps_epoch).days
    weeks_since_epoch = days_since_epoch // 7
    
    # Calculate total seconds since GPS epoch
    total_seconds = weeks_since_epoch * 7 * 24 * 3600 + gps_seconds
    
    # Convert to datetime
    gps_datetime = gps_epoch + timedelta(seconds=total_seconds)
    
    return gps_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
