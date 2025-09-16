#!/usr/bin/env python3
"""
Plot satellites from CSV file
Standalone script for plotting satellite positions from existing CSV files
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import os

def plot_satellites(csv_file, max_epochs=1000, output_file=None):
    """
    Plot satellite positions from CSV file
    
    Parameters:
    -----------
    csv_file : str
        Path to CSV file containing satellite positions
    max_epochs : int
        Maximum number of epochs to plot (for performance)
    output_file : str, optional
        Output PNG file path. If None, uses CSV filename with .png extension
    """
    # Load data
    print(f"Loading data from {csv_file}...")
    data = np.loadtxt(csv_file, delimiter=',')
    
    # Filter out NaN values
    valid_data = data[~np.isnan(data[:, 2])]  # Remove rows where X is NaN
    
    if len(valid_data) == 0:
        print("No valid satellite position data found")
        return
    
    # Limit to max_epochs for performance
    if len(valid_data) > max_epochs:
        valid_data = valid_data[:max_epochs]
        print(f"Limited to first {max_epochs} epochs for performance")
    
    # Separate data by satellite
    satellites = np.unique(valid_data[:, 1])
    print(f"Found {len(satellites)} satellites: {satellites}")
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each satellite
    colors = plt.cm.tab20(np.linspace(0, 1, len(satellites)))
    
    for i, sat in enumerate(satellites):
        sat_data = valid_data[valid_data[:, 1] == sat]
        if len(sat_data) > 0:
            ax.plot(sat_data[:, 2], sat_data[:, 3], sat_data[:, 4], 
                   color=colors[i], linewidth=2, label=f'Sat {int(sat):02d}')
    
    # Set labels and title
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('GPS Satellite Orbits (ECEF Coordinates)')
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Set equal aspect ratio
    max_range = np.array([valid_data[:, 2].max() - valid_data[:, 2].min(),
                         valid_data[:, 3].max() - valid_data[:, 3].min(),
                         valid_data[:, 4].max() - valid_data[:, 4].min()]).max() / 2.0
    mid_x = (valid_data[:, 2].max() + valid_data[:, 2].min()) * 0.5
    mid_y = (valid_data[:, 3].max() + valid_data[:, 3].min()) * 0.5
    mid_z = (valid_data[:, 4].max() + valid_data[:, 4].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    # Determine output filename
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(csv_file))[0]
        output_file = f"results/{base_name}.png"
    
    # Save plot
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved plot: {output_file}")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Plot satellite positions from CSV file")
    parser.add_argument("csv_file", help="Path to CSV file containing satellite positions")
    parser.add_argument("--max_epochs", type=int, default=1000, 
                       help="Maximum number of epochs to plot (default: 1000)")
    parser.add_argument("--output", "-o", help="Output PNG file path")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file '{args.csv_file}' not found!")
        return 1
    
    try:
        plot_satellites(args.csv_file, args.max_epochs, args.output)
        return 0
    except Exception as e:
        print(f"Error plotting satellites: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
