# -*- coding: utf-8 -*-
"""
Satellite Position Calculator
Main Python script for RINEX processing and plotting

@author: Based on MATLAB rinexnav_enhanced.m functionality
"""

import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import georinex as gr
from gpsweekcal import gpsweekcal
from readrinex import readrinex, get_eph
from find_eph import find_eph
from satpos import satpos
from ecef_to_lla import ecef_to_lla
from plot_satellites import plot_satellites

# Parse command line arguments
parser = argparse.ArgumentParser(description="Satellite position calculator with plotting")
parser.add_argument("--file", type=str, default="data/brdc0680.20n", help="RINEX navigation file")
parser.add_argument("--date", type=str, default="20,3,10", help="Date in format YY,MM,DD (like MATLAB)")
parser.add_argument("--interval", type=int, default=15, help="Time interval in seconds")
parser.add_argument("--plot", action="store_true", help="Generate 3D plot of satellite orbits")
parser.add_argument("--max_epochs", type=int, default=1000, help="Maximum epochs to plot")
args = parser.parse_args()


def main():
    print("\n--- Satellite Position Calculator ---")
    print(f"RINEX file: {args.file}")
    print(f"Date: {args.date}")
    print(f"Interval: {args.interval} seconds")
    print(f"Plot: {args.plot}\n")
    
    # Parse date (format: YY,MM,DD like MATLAB)
    date_parts = [int(x.strip()) for x in args.date.split(',')]
    if len(date_parts) != 3:
        raise ValueError("Date must be in format YY,MM,DD")
    
    yy, month, day = date_parts
    # Convert 2-digit year to 4-digit year
    if yy < 86:  # <86 = 20**, >86 = 19**
        year = yy + 2000
    else:
        year = yy + 1900
    
    # Generate time series for 24 hours
    print("Generating time series...")
    mytime = gpsweekcal([year, month, day], args.interval)
    rwt, colt = mytime.shape
    print(f"Generated {rwt} time epochs")
    
    # Load RINEX navigation file
    print("Loading RINEX navigation file...")
    nav_data = readrinex(args.file)
    if nav_data is None:
        print("Failed to load RINEX file")
        return
    
    print(f"Loaded navigation data: {nav_data}")
    
    # Get available satellites
    available_sats = nav_data.sv.values
    print(f"Available satellites: {len(available_sats)} - {available_sats}")
    
    # Process GPS satellites dynamically with 32 threshold
    max_prn = 32  # Maximum GPS PRNs (threshold)
    print(f"Processing up to {max_prn} satellites (1-{max_prn}) with dynamic discovery")
    
    # Initialize arrays for satellite positions
    svposh = np.zeros((max_prn, 5))  # [time, sv, X, Y, Z]
    svposc = []
    
    print("Computing satellite positions...")
    successful_calculations = 0
    
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
                        print(f"Error calculating position for satellite {sv} at time {timesat}: {e}")
                    svposh[j, :] = [timesat, sv, np.nan, np.nan, np.nan]
            else:
                # Satellite not available
                svposh[j, :] = [timesat, sv, np.nan, np.nan, np.nan]
        
        svposc.append(svposh.copy())
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{rwt} epochs...")
    
    print(f"Successful calculations: {successful_calculations}")
    
    # Convert to single array
    svpos = np.vstack(svposc)
    print(f"Computed {svpos.shape[0]} satellite positions")
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Get input filename without extension
    name = os.path.splitext(os.path.basename(args.file))[0]
    
    # Save CSV data
    csv_filename = f'results/{name}.csv'
    np.savetxt(csv_filename, svpos, delimiter=',', fmt='%.10f')
    print(f"✓ Saved: {csv_filename}")
    
    # Also save with lat/lon/alt format
    lla_filename = f'results/{name}_latlonalt.csv'
    lla_data = []
    for row in svpos:
        if not np.isnan(row[2]):  # If X coordinate is not NaN
            lat, lon, alt = ecef_to_lla(row[2], row[3], row[4])
            lla_data.append([row[0], row[1], lat, lon, alt])
        else:
            lla_data.append([row[0], row[1], np.nan, np.nan, np.nan])
    
    lla_array = np.array(lla_data)
    np.savetxt(lla_filename, lla_array, delimiter=',', 
               header='Time,Sat,Lat,Lon,Alt', comments='', fmt='%.10f')
    print(f"✓ Saved: {lla_filename}")
    
    print("\nRINEX Processing Complete!")
    print(f"Data saved to: {csv_filename}")
    print(f"Total epochs processed: {rwt}")
    print(f"Total satellite positions calculated: {svpos.shape[0]}")
    print(f"Number of satellites processed: {max_prn}")
    
    # Generate plot if requested
    if args.plot:
        print("\nGenerating 3D plot...")
        plot_satellites(csv_filename, args.max_epochs)

if __name__ == "__main__":
    main()