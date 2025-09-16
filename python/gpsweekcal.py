# -*- coding: utf-8 -*-
"""
GPS Week Calendar
Based on MATLAB gpsweekcal.m

@author: Based on LEE HONG SHENG's MATLAB implementation
"""

import numpy as np
from julday import julday
from gps_time import gps_time


def gpsweekcal(date, interval):
    """
    Calculate GPS week and generate time for 24 hours
    Based on MATLAB gpsweekcal.m

    Parameters:
    -----------
    date : list
        [year, month, day] in format [YY, MM, DD]
    interval : int
        Time interval in seconds

    Returns:
    --------
    my_time : numpy.ndarray
        Array with [week, time] for each epoch
    """
    year, month, day = date
    # Generate time from 0 to 86399 seconds (24 hours)
    # MATLAB: h = [0:interval:86399]'/3600
    h = np.arange(0, 86400, interval) / 3600  # Hours from 0 to 23.99...
    jd = julday(year, month, day, h)
    week, sec_of_week = gps_time(jd)
    time = np.round(sec_of_week).astype(int)  # Convert to integer seconds
    my_time = np.column_stack((week, time))
    return my_time
