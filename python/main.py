# -*- coding: utf-8 -*-
"""
CLI entry point for RINEX satellite position processing and plotting.
"""

import argparse
import os
import sys

# Allow running as: python3 python/main.py from repo root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plot_satellites import plot_animation, plot_satellites
from rinexnav import process_rinex


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Satellite position calculator with plotting"
    )
    parser.add_argument(
        "--file",
        type=str,
        default="data/brdc0680.20n",
        help="RINEX navigation file",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date in format YY,MM,DD (like MATLAB). If not provided, will be extracted from RINEX file",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Time interval in seconds",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Plot existing CSV instead of processing a RINEX file",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate 3D plot of satellite orbits",
    )
    parser.add_argument(
        "--animation",
        "-a",
        action="store_true",
        help="Create animated plot of satellite orbits",
    )
    parser.add_argument(
        "--format",
        choices=["gif", "mp4"],
        default="gif",
        help="Output format for animation: gif or mp4 (default: gif)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path for plot or animation",
    )
    parser.add_argument(
        "--max_epochs",
        type=int,
        default=1000,
        help="Maximum epochs to plot",
    )
    return parser.parse_args(argv)


def run_plot(csv_file, args):
    """Plot or animate an existing CSV file."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file '{csv_file}' not found")

    if args.animation:
        plot_animation(csv_file, args.max_epochs, args.output, args.format)
    else:
        plot_satellites(csv_file, args.max_epochs, args.output)


def main(argv=None):
    args = parse_args(argv)

    # Plot existing CSV data
    if args.csv is not None:
        run_plot(args.csv, args)
        return

    date = None
    if args.date is not None:
        date_parts = [int(x.strip()) for x in args.date.split(",")]
        if len(date_parts) != 3:
            raise ValueError("Date must be in format YY,MM,DD")
        date = date_parts

    # Process RINEX; plotting handled here so --animation works too
    svpos, csv_filename = process_rinex(
        file_path=args.file,
        date=date,
        interval=args.interval,
        plot=False,
        max_epochs=args.max_epochs,
    )

    if csv_filename is None:
        return

    if args.plot:
        plot_satellites(csv_filename, args.max_epochs, args.output)

    if args.animation:
        plot_animation(csv_filename, args.max_epochs, args.output, args.format)


if __name__ == "__main__":
    main()
