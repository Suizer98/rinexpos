# -*- coding: utf-8 -*-
"""
ECEF to LLA Conversion
Utility function for coordinate conversion

@author: Based on standard geodetic conversion algorithms
"""

import numpy as np


def ecef_to_lla(x, y, z):
    """
    Convert ECEF coordinates to Latitude, Longitude, Altitude

    Parameters:
    -----------
    x, y, z : float or array
        ECEF coordinates in meters

    Returns:
    --------
    lat, lon, alt : float or array
        Latitude, longitude (degrees), altitude (meters)
    """
    a = 6378137.0  # semi-major axis in meters
    e = 8.1819190842622e-2  # eccentricity

    asq = a**2
    esq = e**2

    b = np.sqrt(asq * (1 - esq))
    bsq = b**2
    ep = np.sqrt((asq - bsq) / bsq)
    p = np.sqrt(x**2 + y**2)
    th = np.arctan2(a * z, b * p)

    lon = np.arctan2(y, x)
    lat = np.arctan2((z + ep**2 * b * np.sin(th) ** 3), (p - esq * a * np.cos(th) ** 3))
    N = a / np.sqrt(1 - esq * np.sin(lat) ** 2)
    alt = p / np.cos(lat) - N

    # Convert from radians to degrees
    lon = np.degrees(lon)
    lat = np.degrees(lat)

    return lat, lon, alt
