# -*- coding: utf-8 -*-
"""
CLI entry point for RINEX satellite position processing.
"""

import argparse
import os
import sys

# Allow running as: python3 python/main.py from repo root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        "--plot",
        action="store_true",
        help="Generate 3D plot of satellite orbits",
    )
    parser.add_argument(
        "--max_epochs",
        type=int,
        default=1000,
        help="Maximum epochs to plot",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    date = None
    if args.date is not None:
        date_parts = [int(x.strip()) for x in args.date.split(",")]
        if len(date_parts) != 3:
            raise ValueError("Date must be in format YY,MM,DD")
        date = date_parts

    process_rinex(
        file_path=args.file,
        date=date,
        interval=args.interval,
        plot=args.plot,
        max_epochs=args.max_epochs,
    )


if __name__ == "__main__":
    main()
