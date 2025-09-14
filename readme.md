# RINEX Position Processing

A comprehensive toolkit for processing RINEX (Receiver Independent Exchange Format) GPS navigation and observation files to extract satellite positions and generate 3D orbital visualizations.

## What it does

This project reads RINEX navigation files (`.n` files) containing GPS satellite ephemeris data and calculates satellite positions over time. It then visualizes the complex 3D orbital trajectories of all visible satellites, showing their movement patterns and orbital characteristics.

**Tech stacks:**

![Tech stacks](https://skillicons.dev/icons?i=python,anaconda,matlab,octave,docker)

## Local Setup

### Python

In the project directory, run:

```
conda activate rinex
python3 python/readnav.py
```

#### Installation

Install Anaconda on your pc, then in the project directory, run:

```
conda env create -f environment.yml
```

### MATLAB/Octave

In the project directory, run:

```
octave --eval "rinexnav"
```

#### Installation

Install octave on your linux environment:

```
apt-get update -y --no-install-recommends \
apt-get install -y --no-install-recommends \
    octave \
    octave-netcdf \
    libnetcdf-dev \
```

## Docker Setup

### Quick Start

Build and run the container:

```bash
docker-compose up --build
```

### Running Commands

Execute Python code:
```bash
docker-compose exec rinexpos python3 python/readnav.py
```

Execute Octave/MATLAB code:
```bash
docker-compose exec rinexpos bash -c "cd matlab && octave rinexnav.m"
```

## Sample Results

![Sample Satellite Orbits](results/chur1610.png)

*3D visualization of GPS satellite orbits showing the complex trajectories of 29 satellites over time, with each satellite represented by a unique colored line.*
