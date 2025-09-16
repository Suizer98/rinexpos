# -*- coding: utf-8 -*-
"""
GPS Time Check and Repair
Based on MATLAB check_t.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np


def check_t(t):
    """
    Repairs over- and underflow of GPS time
    Based on MATLAB check_t.m
    
    Parameters:
    -----------
    t : float or array
        GPS time in seconds
        
    Returns:
    --------
    tt : float or array
        Corrected GPS time
    """
    half_week = 302400
    tt = t
    if t > half_week:
        tt = t - 2 * half_week
    if t < -half_week:
        tt = t + 2 * half_week
    return tt
