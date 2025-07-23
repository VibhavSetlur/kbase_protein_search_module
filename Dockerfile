FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# -----------------------------------------
# Fix for EOL Debian Stretch (cover all possible URLs)
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://httpredir.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org|http://archive.debian.org|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    sed -i '/stretch\/updates/d' /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until
# -----------------------------------------

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip==21.3.1 setuptools==59.5.0 wheel

# Install required Python dependencies
RUN pip install --no-cache-dir \
    numpy==1.21.0 \
    pandas==1.3.0 \
    h5py==3.6.0 \
    pyarrow==6.0.0 \
    tables==3.7.0 \
    zarr==2.10.3 \
    joblib==1.1.0 \
    tqdm==4.62.0 \
    pyyaml==6.0

# Copy the module code
COPY ./ /kb/module
RUN python3 /kb/module/scripts/generate_dummy_data.py
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

# Build the module
RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
