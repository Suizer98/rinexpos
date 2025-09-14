FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables for non-interactive apt and Octave
ENV DEBIAN_FRONTEND=noninteractive \
    OCTAVE_NO_GUI=true \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies and Octave
RUN set -xe \
    && apt-get update -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        octave \
        octave-netcdf \
        libnetcdf-dev \
        python3-pip \
        python3.10 \
        python3.10-dev \
        build-essential \
        libhdf5-dev \
        pkg-config \
        wget \
        curl \
        ghostscript \
        gnuplot \
        libcairo2-dev \
        libpango1.0-dev \
        ghostscript \
        gnuplot \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy fonts
COPY freesans/ /usr/share/fonts/opentype/freefont/
RUN fc-cache -fv

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]