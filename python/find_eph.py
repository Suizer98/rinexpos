# -*- coding: utf-8 -*-
"""
Find Ephemeris
Based on MATLAB find_eph.m

@author: Based on Kai Borre's MATLAB implementation
"""

import numpy as np


def find_eph(Eph, sv, time):
    """
    Find the proper ephemeris data for a satellite at a given time
    Works with both georinex xarray format and MATLAB array format

    Parameters:
    -----------
    Eph : xarray.Dataset or numpy.ndarray
        Ephemeris data
    sv : int
        Satellite number
    time : float
        GPS time in seconds

    Returns:
    --------
    eph_data : xarray.Dataset or numpy.ndarray
        Ephemeris data for the satellite, or None if not found
    """
    if hasattr(Eph, "data_vars"):
        # Handle georinex xarray format
        sv_str = f"G{sv:02d}"

        # Check if satellite exists in the dataset
        if sv_str not in Eph.sv.values:
            return None

        # Get all time epochs for this satellite
        sat_data = Eph.sel(sv=sv_str)

        # Find the most recent ephemeris before or at the given time
        # First, get all valid (non-NaN) ephemeris records
        valid_indices = []
        toe_values = []
        for i, t in enumerate(sat_data.time.values):
            if not np.isnan(sat_data["Toe"].isel(time=i).values):
                valid_indices.append(i)
                toe_values.append(sat_data["Toe"].isel(time=i).values)

        if not valid_indices:
            return None

        # Convert time to GPS seconds of week for comparison
        # GPS time is seconds since GPS epoch (1980-01-06 00:00:00 UTC)
        # For this comparison, we'll use the Toe values directly

        # Find the earliest ephemeris (like MATLAB)
        earliest_idx = valid_indices[0]
        earliest_toe = toe_values[0]

        for i, idx in enumerate(valid_indices):
            if toe_values[i] < earliest_toe:
                earliest_idx = idx
                earliest_toe = toe_values[i]

        # Find the most recent ephemeris before or at the given time
        best_idx = earliest_idx
        best_toe_diff = earliest_toe - time

        for i, idx in enumerate(valid_indices):
            toe_diff = toe_values[i] - time
            if toe_diff <= 0:  # Before or at the given time
                if abs(toe_diff) < abs(best_toe_diff):
                    best_idx = idx
                    best_toe_diff = toe_diff

        closest_idx = best_idx

        # Return the ephemeris data for this time
        return sat_data.isel(time=closest_idx)

    else:
        # Handle MATLAB array format
        icol = 0
        isat = np.where(Eph[0, :] == sv)[
            0
        ]  # Find columns with matching satellite number

        if len(isat) == 0:
            return None

        icol = isat[0]
        dtmin = Eph[20, icol]  # Time of clock (toc)

        # Find the earliest ephemeris
        for t in isat:
            dtest = Eph[20, t]
            if dtest < dtmin:
                icol = t
                dtmin = dtest

        # Find the most recent ephemeris before the given time
        dtmin = Eph[20, icol] - time
        for t in isat:
            dt = Eph[20, t] - time
            if dt < 0:
                if abs(dt) < abs(dtmin):
                    icol = t
                    dtmin = dt

        return Eph[:, icol] if icol >= 0 else None
