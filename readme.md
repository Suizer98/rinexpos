# Rinex Pos

A simple project to get time series satellite position from RINEX navigation and observation file

Tech stacks:

![Tech stacks](https://skillicons.dev/icons?i=python,anaconda,matlab,octave)

## Python

In the project directory, run:

```
conda activate rinex
python3 readnav.py
```

### Installation

Install Anaconda on your pc, then in the project directory, run:

```
conda env create -f environment.yml
```

## Matlab

In the project directory, run:

```
octave --eval "rinexnav"
```

### Installation

Install octave on your linux environment:

```
    apt-get update -y --no-install-recommends \
    apt-get install -y --no-install-recommends \
        octave \
        octave-netcdf \
        libnetcdf-dev \
```
