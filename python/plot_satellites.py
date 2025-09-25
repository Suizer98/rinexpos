#!/usr/bin/env python3
"""
Plot satellites from CSV file
Standalone script for plotting satellite positions from existing CSV files
"""

import argparse
import os

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def load_and_prepare_data(csv_file, max_epochs=1000):
    """Load and prepare satellite data from CSV file"""
    print(f"Loading data from {csv_file}...")
    data = np.loadtxt(csv_file, delimiter=",")

    # Filter out NaN values
    valid_data = data[~np.isnan(data[:, 2])]  # Remove rows where X is NaN

    if len(valid_data) == 0:
        print("No valid satellite position data found")
        return None, None, None

    # Limit to max_epochs for performance
    unique_times = np.unique(valid_data[:, 0])
    if len(unique_times) > max_epochs:
        selected_times = unique_times[:max_epochs]
        valid_data = valid_data[np.isin(valid_data[:, 0], selected_times)]
        # Recalculate unique_times after filtering
        unique_times = np.unique(valid_data[:, 0])
        print(f"Limited to first {max_epochs} epochs ({len(valid_data)} data points)")

    satellites = np.unique(valid_data[:, 1])
    print(f"Found {len(satellites)} satellites: {satellites}")

    return valid_data, satellites, unique_times


def setup_3d_plot(figsize=(12, 10)):
    """Create and configure 3D plot"""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    # Set labels
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    return fig, ax


def set_plot_limits(ax, valid_data):
    """Set equal aspect ratio for 3D plot"""
    max_range = (
        np.array(
            [
                valid_data[:, 2].max() - valid_data[:, 2].min(),
                valid_data[:, 3].max() - valid_data[:, 3].min(),
                valid_data[:, 4].max() - valid_data[:, 4].min(),
            ]
        ).max()
        / 2.0
    )
    mid_x = (valid_data[:, 2].max() + valid_data[:, 2].min()) * 0.5
    mid_y = (valid_data[:, 3].max() + valid_data[:, 3].min()) * 0.5
    mid_z = (valid_data[:, 4].max() + valid_data[:, 4].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)


def get_output_filename(csv_file, output_file, suffix="", ext="png"):
    """Generate output filename"""
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(csv_file))[0]
        output_file = f"results/{base_name}{suffix}.{ext}"
    return output_file


def plot_satellites(csv_file, max_epochs=1000, output_file=None):
    """Plot satellite positions from CSV file"""
    # Load and prepare data
    valid_data, satellites, _ = load_and_prepare_data(csv_file, max_epochs)
    if valid_data is None:
        return

    # Setup plot
    fig, ax = setup_3d_plot()
    colors = plt.cm.tab20(np.linspace(0, 1, len(satellites)))

    # Plot each satellite
    for i, sat in enumerate(satellites):
        sat_data = valid_data[valid_data[:, 1] == sat]
        if len(sat_data) > 0:
            sat_data = sat_data[sat_data[:, 0].argsort()]  # Sort by time

            if len(sat_data) > 10:
                ax.plot(
                    sat_data[:, 2],
                    sat_data[:, 3],
                    sat_data[:, 4],
                    color=colors[i],
                    linewidth=1.5,
                    label=f"Sat {int(sat):02d}",
                    alpha=0.8,
                )
            else:
                ax.scatter(
                    sat_data[:, 2],
                    sat_data[:, 3],
                    sat_data[:, 4],
                    color=colors[i],
                    s=20,
                    label=f"Sat {int(sat):02d}",
                    alpha=0.6,
                )

    # Configure plot
    ax.set_title("GPS Satellite Orbits (ECEF Coordinates)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    set_plot_limits(ax, valid_data)

    # Save plot
    output_file = get_output_filename(csv_file, output_file)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Saved plot: {output_file}")
    return output_file


def plot_animation(csv_file, max_epochs=1000, output_file=None, format="gif"):
    """Create animated plot of satellite positions from CSV file"""
    # Load and prepare data
    valid_data, satellites, unique_times = load_and_prepare_data(csv_file, max_epochs)
    if valid_data is None:
        return

    # Setup plot
    fig, ax = setup_3d_plot()
    colors = plt.cm.tab20(np.linspace(0, 1, len(satellites)))

    # Prepare satellite data for animation
    sat_data_dict = {}
    sat_indices = {}
    valid_satellites = []

    for sat in satellites:
        sat_data = valid_data[valid_data[:, 1] == sat]
        if len(sat_data) > 0:
            sat_data = sat_data[sat_data[:, 0].argsort()]
            sat_data_dict[sat] = sat_data
            sat_indices[sat] = len(valid_satellites)
            valid_satellites.append(sat)

    # Initialize animation elements
    lines, points = [], []
    for i, sat in enumerate(valid_satellites):
        (line,) = ax.plot(
            [],
            [],
            [],
            color=colors[i],
            linewidth=2,
            label=f"Sat {int(sat):02d}",
            alpha=0.8,
        )
        lines.append(line)

        (point,) = ax.plot([], [], [], "o", color=colors[i], markersize=8, alpha=1.0)
        points.append(point)

    # Configure plot
    ax.set_title("GPS Satellite Orbits Animation (ECEF Coordinates)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    set_plot_limits(ax, valid_data)

    def animate(frame):
        current_time = unique_times[frame]

        for sat in valid_satellites:
            if sat in sat_data_dict:
                sat_data = sat_data_dict[sat]
                i = sat_indices[sat]

                time_mask = sat_data[:, 0] <= current_time
                current_data = sat_data[time_mask]

                if len(current_data) > 0:
                    lines[i].set_data_3d(
                        current_data[:, 2], current_data[:, 3], current_data[:, 4]
                    )

                    # Convert scalars to arrays for set_data_3d
                    x_pos = np.array([current_data[-1, 2]])
                    y_pos = np.array([current_data[-1, 3]])
                    z_pos = np.array([current_data[-1, 4]])
                    points[i].set_data_3d(x_pos, y_pos, z_pos)

        ax.set_title(
            f"GPS Satellite Orbits Animation (ECEF Coordinates) - Time: {current_time:.1f}"
        )
        return lines + points

    # Create and save animation
    try:
        anim = animation.FuncAnimation(
            fig, animate, frames=len(unique_times), interval=42, blit=False, repeat=True
        )

        output_file = get_output_filename(csv_file, output_file, "_animation", format)
        print(f"Saving animation to {output_file}...")

        if format == "mp4":
            try:
                anim.save(output_file, writer="ffmpeg", fps=24, bitrate=1800)
            except Exception as e:
                print(f"MP4 writer failed, falling back to GIF: {e}")
                output_file = output_file.replace(".mp4", ".gif")
                anim.save(output_file, writer="pillow", fps=24)
        else:
            anim.save(output_file, writer="pillow", fps=24)

        print(f"Saved animation: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error creating/saving animation: {e}")
        import traceback

        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Plot satellite positions from CSV file"
    )
    parser.add_argument(
        "csv_file", help="Path to CSV file containing satellite positions"
    )
    parser.add_argument(
        "--max_epochs",
        type=int,
        default=1000,
        help="Maximum number of epochs to plot (default: 1000)",
    )
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--animation",
        "-a",
        action="store_true",
        help="Create animated plot instead of static plot",
    )
    parser.add_argument(
        "--format",
        choices=["gif", "mp4"],
        default="gif",
        help="Output format for animation: gif or mp4 (default: gif)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file '{args.csv_file}' not found!")
        return 1

    try:
        if args.animation:
            plot_animation(args.csv_file, args.max_epochs, args.output, args.format)
        else:
            plot_satellites(args.csv_file, args.max_epochs, args.output)
        return 0
    except Exception as e:
        print(f"Error plotting satellites: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
