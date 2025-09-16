# RINEX Position Processing

A toolkit for processing RINEX (Receiver Independent Exchange Format) GPS navigation and observation files to extract satellite positions and generate 3D orbital visualizations.

This project reads RINEX navigation files (`.n` files) containing GPS satellite ephemeris data.

**Tech stacks:**

![Tech stacks](https://skillicons.dev/icons?i=python,anaconda,matlab,octave,docker,bash)

## Local Setup

### Python

1. Install Anaconda on your PC
2. Create the environment and install dependencies:
   ```bash
   conda create -n rinex python=3.10
   conda activate rinex
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   conda activate rinex
   python3 python/rinexnav.py --file=data/chur1610.19n --interval=15 --plot
   ```

### MATLAB/Octave

1. Install Octave and dependencies on your system (Linux or WSL2):
   ```bash
   sudo apt-get update -y --no-install-recommends
   sudo apt-get install -y --no-install-recommends \
       octave \
       octave-netcdf \
       libnetcdf-dev \
       gnuplot \
       ghostscript \
       libcairo2-dev \
       libpango1.0-dev
   ```
2. Run the script:
   ```bash
   cd matlab
   octave rinexnav_enhanced.m
   ```

## Docker Setup

### Quick Start

Build and run the container:

```bash
docker-compose up --build
```

Execute Octave/MATLAB code:
```bash
docker-compose exec rinexpos bash -c "cd matlab && octave rinexnav_enhanced.m"
```

Execute Python code:
```bash
docker-compose exec rinexpos python3 python/rinexnav.py --file=data/chur1610.19n --interval=15 --plot
```

Execute Python code with explicit date (if needed):
```bash
docker-compose exec rinexpos python3 python/rinexnav.py --file=data/brdc0680.20n --date=20,3,8 --interval=15 --plot
```

Plot existing CSV data explicitly:
```bash
docker-compose exec rinexpos python3 python/plot_satellites.py results/chur1610_python.csv --max_epochs=1000
```

### Run black formatting

To run code formatting for python files:
```bash
docker-compose exec rinexpos black python/
```

## Sample Results

*3D visualization of GPS satellite orbits showing the complex trajectories of satellites over time, with each satellite represented by a unique colored line. Both are showing the first 1000 epoch from the derieved data*

### MATLAB

![MATLAB](results/chur1610_matlab.png)

### Python

![Python](results/chur1610_python.png)