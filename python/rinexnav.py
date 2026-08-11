# -*- coding: utf-8 -*-
"""
Satellite Position Calculator
RINEX navigation processing based on MATLAB rinexnav_enhanced.m

@author: Based on MATLAB rinexnav_enhanced.m functionality
"""

import os
import time

import numpy as np
from ecef_to_lla import ecef_to_lla
from find_eph import find_eph
from gps_time import gps_time_to_datetime_iso
from gpsweekcal import gpsweekcal
from plot_satellites import plot_satellites
from readrinex import readrinex
from satpos import satpos


def extract_date_from_rinex(file_path):
    """
    Extract the start date from RINEX navigation file
    Based on the first data line format: SV YY MM DD HH MM SS ...

    Parameters:
    -----------
    file_path : str
        Path to RINEX navigation file

    Returns:
    --------
    date : list
        [year, month, day] in format [YY, MM, DD]
    """
    try:
        with open(file_path) as f:
            # Skip header lines until we find the first data line
            for line in f:
                line = line.strip()
                # Check if this is a data line (starts with satellite number and has proper format)
                # Format: SV YY MM DD HH MM SS ...
                if line and len(line) > 20:
                    parts = line.split()
                    # Check if we have enough parts and first part is a satellite number
                    if len(parts) >= 6 and parts[0].isdigit():
                        try:
                            yy = int(parts[1])
                            month = int(parts[2])
                            day = int(parts[3])
                            return [yy, month, day]
                        except ValueError:
                            # Skip this line if parsing fails
                            continue

        # If no data line found, return None
        return None

    except Exception as e:
        print(f"Error extracting date from RINEX file: {e}")
        return None


def yy_to_year(yy):
    """Convert 2-digit year to 4-digit year (<86 = 20**, >=86 = 19**)."""
    # <86 = 20**, >=86 = 19**
    if yy < 86:
        return yy + 2000
    return yy + 1900


def format_elapsed(seconds):
    """Format elapsed seconds as e.g. 45s, 10m, or 10m 5s."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    if secs == 0:
        return f"{minutes}m"
    return f"{minutes}m {secs}s"


def compute_svpos(nav_data, mytime, max_prn=32):
    """
    Compute satellite ECEF positions for all epochs and PRNs 1..max_prn.

    Parameters:
    -----------
    nav_data : xarray.Dataset
        Navigation data from readrinex
    mytime : numpy.ndarray
        Time series from gpsweekcal, columns [week, sow]
    max_prn : int
        Maximum GPS PRN number (default 32)

    Returns:
    --------
    svpos : numpy.ndarray
        Stacked positions [time, sv, X, Y, Z] for all epochs
    successful_calculations : int
        Number of successful satpos evaluations
    """
    available_sats = nav_data.sv.values
    rwt = mytime.shape[0]

    # Initialize arrays for satellite positions [time, sv, X, Y, Z]
    svposh = np.zeros((max_prn, 5))
    svposc = []
    successful_calculations = 0
    start_time = time.perf_counter()

    for i in range(rwt):
        timesat = mytime[i, 1]  # GPS seconds of week

        for j in range(max_prn):
            sv = j + 1  # Satellite number (1-32)
            sat_id = f"G{sv:02d}"  # Format as G01, G02, etc.

            if sat_id in available_sats:
                try:
                    # Find the correct ephemeris data for this satellite and time
                    eph_single = find_eph(nav_data, sv, timesat)

                    if eph_single is not None:
                        satposition = satpos(timesat, eph_single)
                        X, Y, Z = satposition[0], satposition[1], satposition[2]
                        svposh[j, :] = [timesat, sv, X, Y, Z]
                        successful_calculations += 1
                    else:
                        svposh[j, :] = [timesat, sv, np.nan, np.nan, np.nan]
                except Exception as e:
                    if i < 5 and j < 5:  # Only print first few errors
                        print(
                            f"Error calculating position for satellite {sv} at time {timesat}: {e}"
                        )
                    svposh[j, :] = [timesat, sv, np.nan, np.nan, np.nan]
            else:
                # Satellite not available
                svposh[j, :] = [timesat, sv, np.nan, np.nan, np.nan]

        svposc.append(svposh.copy())

        # Progress every 1000 epochs, and always at the last epoch
        done = i + 1
        if done % 1000 == 0 or done == rwt:
            elapsed = format_elapsed(time.perf_counter() - start_time)
            print(f"Processed {done}/{rwt} epochs [{elapsed}]", flush=True)

    # Convert to single array
    return np.vstack(svposc), successful_calculations


def save_svpos_csv(svpos, name, year, month, day, results_dir="results"):
    """
    Save ECEF and lat/lon/alt CSV results.

    Returns:
    --------
    csv_filename : str
        Path to ECEF CSV
    lla_filename : str
        Path to lat/lon/alt CSV
    """
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)

    # Save CSV data (ECEF: time, sv, X, Y, Z)
    csv_filename = f"{results_dir}/{name}_ecef.csv"
    np.savetxt(csv_filename, svpos, delimiter=",", fmt="%.10f")
    print(f"✓ Saved: {csv_filename}")

    # Also save with lat/lon/alt format with readable dates
    lla_filename = f"{results_dir}/{name}_latlonalt.csv"
    lla_data = []
    for row in svpos:
        # Convert GPS time to readable datetime
        readable_time = gps_time_to_datetime_iso(row[0], year, month, day)
        if not np.isnan(row[2]):  # If X coordinate is not NaN
            lat, lon, alt = ecef_to_lla(row[2], row[3], row[4])
            lla_data.append([readable_time, int(row[1]), lat, lon, alt])
        else:
            lla_data.append([readable_time, int(row[1]), np.nan, np.nan, np.nan])

    # Save as CSV with proper formatting
    with open(lla_filename, "w") as f:
        f.write("Sat,Lat,Lon,Alt,Date\n")
        for row in lla_data:
            if np.isnan(row[2]):  # If lat is NaN
                f.write(f"{row[1]},,,,{row[0]}\n")
            else:
                f.write(
                    f"{row[1]},{row[2]:.10f},{row[3]:.10f},{row[4]:.10f},{row[0]}\n"
                )
    print(f"✓ Saved: {lla_filename}")

    return csv_filename, lla_filename


def process_rinex(
    file_path,
    date=None,
    interval=15,
    plot=False,
    max_epochs=1000,
    max_prn=32,
):
    """
    Process a RINEX navigation file and compute satellite positions.

    Parameters:
    -----------
    file_path : str
        Path to RINEX navigation file
    date : list or None
        [YY, MM, DD]. If None, extracted from the RINEX file
    interval : int
        Time interval in seconds
    plot : bool
        Generate 3D plot of satellite orbits
    max_epochs : int
        Maximum epochs to plot
    max_prn : int
        Maximum GPS PRN number

    Returns:
    --------
    svpos : numpy.ndarray
        Satellite positions [time, sv, X, Y, Z]
    csv_filename : str
        Path to saved ECEF CSV
    """
    print("\n--- Satellite Position Calculator ---")
    print(f"RINEX file: {file_path}")
    print(f"Interval: {interval} seconds")
    print(f"Plot: {plot}\n")

    # Determine date - either provided or extract from RINEX file
    if date is not None:
        # Date format: [YY, MM, DD] like MATLAB
        if len(date) != 3:
            raise ValueError("Date must be [YY, MM, DD]")
        yy, month, day = date
        print(f"Using provided date: {yy},{month},{day}")
    else:
        # Extract date from RINEX file
        print("Extracting date from RINEX file...")
        date_parts = extract_date_from_rinex(file_path)
        if date_parts is None:
            raise ValueError(
                "Could not extract date from RINEX file. Please provide date."
            )
        yy, month, day = date_parts
        print(f"Extracted date from RINEX: {yy},{month},{day}")

    # Convert 2-digit year to 4-digit year
    year = yy_to_year(yy)

    # Generate time series for 24 hours
    print("Generating time series...")
    mytime = gpsweekcal([year, month, day], interval)
    rwt = mytime.shape[0]
    print(f"Generated {rwt} time epochs")

    # Load RINEX navigation file
    print("Loading RINEX navigation file...")
    nav_data = readrinex(file_path)
    if nav_data is None:
        print("Failed to load RINEX file")
        return None, None

    print(f"Loaded navigation data: {nav_data}")

    # Get available satellites
    available_sats = nav_data.sv.values
    print(f"Available satellites: {len(available_sats)} - {available_sats}")

    # Process GPS satellites dynamically with 32 threshold
    # Maximum GPS PRNs (threshold)
    print(f"Processing up to {max_prn} satellites (1-{max_prn}) with dynamic discovery")

    print("Computing satellite positions...")
    svpos, successful_calculations = compute_svpos(nav_data, mytime, max_prn=max_prn)
    print(f"Successful calculations: {successful_calculations}")
    print(f"Computed {svpos.shape[0]} satellite positions")

    # Get input filename without extension
    name = os.path.splitext(os.path.basename(file_path))[0]
    csv_filename, lla_filename = save_svpos_csv(svpos, name, year, month, day)

    print("\nRINEX Processing Complete!")
    print(f"Data saved to: {csv_filename}")
    print(f"LLA data saved to: {lla_filename}")
    print(f"Total epochs processed: {rwt}")
    print(f"Total satellite positions calculated: {svpos.shape[0]}")
    print(f"Number of satellites processed: {max_prn}")

    # Generate plot if requested
    if plot:
        print("\nGenerating 3D plot...")
        plot_satellites(csv_filename, max_epochs)

    return svpos, csv_filename
