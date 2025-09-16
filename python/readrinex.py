# -*- coding: utf-8 -*-
"""
Read RINEX Navigation File
Based on MATLAB rinexe.m and get_eph.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np
import georinex as gr


def readrinex(file):
    """
    Read RINEX navigation file using georinex
    Based on MATLAB rinexe.m and get_eph.m
    
    Parameters:
    -----------
    file : str
        Path to RINEX navigation file
        
    Returns:
    --------
    nav_data : xarray.Dataset
        Navigation data loaded by georinex
    """
    try:
        nav_data = gr.load(file)
        return nav_data
    except Exception as e:
        print(f"Error loading RINEX file {file}: {e}")
        return None


def get_eph(nav_data, sv=None):
    """
    Extract ephemeris data for specific satellite
    Based on MATLAB get_eph.m
    
    Parameters:
    -----------
    nav_data : xarray.Dataset
        Navigation data from georinex
    sv : str, optional
        Satellite ID (e.g., 'G01'). If None, returns all satellites
        
    Returns:
    --------
    eph : xarray.Dataset
        Ephemeris data for the specified satellite
    """
    if sv is None:
        return nav_data
    else:
        return nav_data.sel(sv=sv).dropna(dim="time", how="all")
