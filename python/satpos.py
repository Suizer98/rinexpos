# -*- coding: utf-8 -*-
"""
Satellite Position Calculation
Based on MATLAB satpos.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np
from check_t import check_t

# Constants
GM = 3.986005e14  # Earth's universal gravitational parameter m^3/s^2
omegae_dot = 7.2921151467e-5  # Earth rotation rate rad/s


def satpos(t, eph):
    """
    Calculate X,Y,Z coordinates at time t for given ephemeris
    Based on MATLAB satpos.m

    Parameters:
    -----------
    t : float
        GPS time in seconds
    eph : dict or array
        Ephemeris data containing satellite parameters

    Returns:
    --------
    satp : numpy.ndarray
        [X, Y, Z] coordinates in meters
    """
    # Extract ephemeris parameters
    if hasattr(eph, "data_vars"):
        # Handle georinex xarray format
        # svprn = 0  # Not used in calculation (kept for reference)

        def safe_get(var_name, default=0):
            if var_name in eph:
                val = eph[var_name].values
                if val.ndim == 0:  # Scalar
                    return val.item()
                else:  # Array
                    return val[0]
            return default

        # af2 = safe_get("SVclockDriftRate")  # Unused but kept for reference
        M0 = safe_get("M0")
        roota = safe_get("sqrtA")  # sqrtA is already the square root of semi-major axis
        deltan = safe_get("DeltaN")
        ecc = safe_get("Eccentricity")
        omega = safe_get("omega")
        cuc = safe_get("Cuc")
        cus = safe_get("Cus")
        crc = safe_get("Crc")
        crs = safe_get("Crs")
        i0 = safe_get("Io")
        idot = safe_get("IDOT")
        cic = safe_get("Cic")
        cis = safe_get("Cis")
        Omega0 = safe_get("Omega0")
        Omegadot = safe_get("OmegaDot")
        toe = safe_get("Toe")
        # af0 = safe_get("SVclockBias")  # Unused but kept for reference
        # af1 = safe_get("SVclockDrift")  # Unused but kept for reference
    elif isinstance(eph, dict):
        # Handle dictionary format
        # svprn = eph.get("SVclockBias", 0)  # Unused but kept for reference
        # af2 = eph.get("SVclockDriftRate", 0)  # Unused but kept for reference
        M0 = eph.get("M0", 0)
        roota = eph.get(
            "sqrtA", 0
        )  # sqrtA is already the square root of semi-major axis
        deltan = eph.get("DeltaN", 0)
        ecc = eph.get("Eccentricity", 0)
        omega = eph.get("omega", 0)
        cuc = eph.get("Cuc", 0)
        cus = eph.get("Cus", 0)
        crc = eph.get("Crc", 0)
        crs = eph.get("Crs", 0)
        i0 = eph.get("Io", 0)
        idot = eph.get("IDOT", 0)
        cic = eph.get("Cic", 0)
        cis = eph.get("Cis", 0)
        Omega0 = eph.get("Omega0", 0)
        Omegadot = eph.get("OmegaDot", 0)
        toe = eph.get("Toe", 0)
        # toc = eph.get("Toe", 0)  # Time of clock (unused but kept for reference)
        # af0 = eph.get("SVclockBias", 0)  # Unused but kept for reference
        # af1 = eph.get("SVclockDrift", 0)  # Unused but kept for reference
    else:
        # Handle array format (MATLAB style)
        M0 = eph[2]
        roota = eph[3]
        deltan = eph[4]
        ecc = eph[5]
        omega = eph[6]
        cuc = eph[7]
        cus = eph[8]
        crc = eph[9]
        crs = eph[10]
        i0 = eph[11]
        idot = eph[12]
        cic = eph[13]
        cis = eph[14]
        Omega0 = eph[15]
        Omegadot = eph[16]
        toe = eph[17]
        # toc = eph[20]  # Time of clock (unused but kept for reference)

    # Procedure for coordinate calculation (Keplerian elements)
    A = roota * roota  # Semi-major axis (roota is sqrt(A))
    tk = check_t(t - toe)
    n0 = np.sqrt(GM / A**3)
    n = n0 + deltan
    M = M0 + n * tk
    M = np.mod(M + 2 * np.pi, 2 * np.pi)

    # Solve Kepler's equation
    E = M
    for _ in range(10):
        E_old = E
        E = M + ecc * np.sin(E)
        dE = np.mod(E - E_old, 2 * np.pi)
        if abs(dE) < 1e-12:
            break

    E = np.mod(E + 2 * np.pi, 2 * np.pi)
    v = np.arctan2(np.sqrt(1 - ecc**2) * np.sin(E), np.cos(E) - ecc)
    phi = v + omega
    phi = np.mod(phi, 2 * np.pi)

    u = phi + cuc * np.cos(2 * phi) + cus * np.sin(2 * phi)
    r = A * (1 - ecc * np.cos(E)) + crc * np.cos(2 * phi) + crs * np.sin(2 * phi)
    i = i0 + idot * tk + cic * np.cos(2 * phi) + cis * np.sin(2 * phi)
    Omega = Omega0 + (Omegadot - omegae_dot) * tk - omegae_dot * toe
    Omega = np.mod(Omega + 2 * np.pi, 2 * np.pi)

    x1 = np.cos(u) * r
    y1 = np.sin(u) * r

    satp = np.zeros(3)
    satp[0] = x1 * np.cos(Omega) - y1 * np.cos(i) * np.sin(Omega)
    satp[1] = x1 * np.sin(Omega) + y1 * np.cos(i) * np.cos(Omega)
    satp[2] = y1 * np.sin(i)

    return satp
