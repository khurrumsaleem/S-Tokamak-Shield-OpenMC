# =============================================================================
# Dockerfile
#
# Recreates the fusion-energy/neutronics-workshop (ghcr.io/fusion-energy/
# neutronics-workshop) environment for the Spherical Tokamak shielding
# study (vvij_ptnr_2023.ipynb (https://github.com/light0vij/Tokomak-Radiation-Shielding-Material-Optimization_OpenMc_Fusion_Pramak)) — WITHOUT compiling 
# OpenMC/MOAB/DAGMC/
# Embree/Double-Down from source.
#
# OpenMC (with DAGMC support) and MOAB (pymoab) are installed from
# Jonathan Shimwell's community wheel index, exactly as the workshop's own
# tooling recommends:
#
#   pip install --extra-index-url https://shimwell.github.io/wheels openmc
#
# Those wheels are built for CPython 3.12 on manylinux_2_28. ubuntu:24.04
# (noble) ships Python 3.12 natively, so -- unlike ubuntu:22.04, which needs
# the deadsnakes PPA and a manual get-pip.py bootstrap to reach 3.12 -- no
# extra Python-version workaround is needed here at all.
#
# Nuclear data (ENDF/B-VIII.0 cross sections + WMP library) is intentionally
# NOT baked into this image, to keep it small. It is downloaded separately,
# on first container start.
#
# Run (mount a host folder for nuclear_data so the ~2GB download only
# happens once, and a folder for your notebooks/outputs):
#   docker run -p 8888:8888 \
#       -v $PWD/nuclear_data:/nuclear_data \
#       -v $PWD/notebooks:/home/neutronics/notebooks \
#       s-tokamak-shield-openmc
# =============================================================================

FROM ubuntu:24.04

LABEL maintainer="light0vij" \
      description="NEUTRONICS ANALYSIS TO OPTIMISE NEUTRON SHIELDING MATERIALS IN SPHERICAL TOKAMAK USING OPENMC"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1

# ---------------------------------------------------------------------------
# System dependencies
#   - python3 / python3-pip / python3-venv: ubuntu:24.04 ships Python 3.12
#     natively, which is exactly what the shimwell cp312 wheels (openmc,
#     moab) need -- no PPA or manual pip bootstrap required.
#   - OpenGL / Mesa / X libs: needed for CadQuery / paramak / gmsh headless
#     geometry rendering and SVG/STL export.
#   - libhdf5: OpenMC's statepoint/summary files are HDF5.
#   - git/wget/curl: used by the nuclear-data download step and some pip
#     packages that fetch resources at install time.
# ---------------------------------------------------------------------------
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        wget \
        curl \
        git \
        ca-certificates \
        libgl1 \
        libglu1-mesa \
        libglx-mesa0 \
        freeglut3-dev \
        libosmesa6 \
        libgles2 \
        libxrender1 \
        libxcursor1 \
        libxft2 \
        libxinerama1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libhdf5-dev \
        imagemagick && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3 /usr/local/bin/python

# ---------------------------------------------------------------------------
# Python (pip / wheel) dependencies
#   openmc + moab are pulled from shimwell's DAGMC-enabled wheel index
#   (declared via --extra-index-url inside requirements.txt itself);
#   everything else resolves from normal PyPI.
# ---------------------------------------------------------------------------
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
        rm /tmp/requirements.txt

# ---------------------------------------------------------------------------
# Project files
# ---------------------------------------------------------------------------
WORKDIR /home/neutronics
#COPY materials.py /home/neutronics/materials.py
COPY notebooks/ /home/neutronics/notebooks/

# Nuclear data lives outside the image (downloaded on first run into this
# mount point) to keep the image lean -- see executedownload.sh / README.
ENV OPENMC_CROSS_SECTIONS=/nuclear_data/cross_sections.xml \
    OPENMC_CHAIN_FILE=/nuclear_data/chain-endf-b8.0.xml
RUN mkdir -p /nuclear_data

# ---------------------------------------------------------------------------
# JupyterLab configuration
# ---------------------------------------------------------------------------
RUN jupyter lab --generate-config && \
    printf '%s\n' \
        "c.ServerApp.ip = '0.0.0.0'" \
        "c.ServerApp.port = 8888" \
        "c.ServerApp.open_browser = False" \
        "c.ServerApp.token = ''" \
        "c.ServerApp.password = ''" \
        "c.ServerApp.allow_root = True" \
        "c.ServerApp.root_dir = '/home/neutronics/notebooks'" \
        >> /root/.jupyter/jupyter_lab_config.py

# executedownload.sh lives at the container root, not under WORKDIR, so it
# never appears in the Jupyter file browser either.
COPY executedownload.sh /executedownload.sh
RUN chmod +x /executedownload.sh

EXPOSE 8888

# executedownload.sh downloads the nuclear data (once) then launches
# JupyterLab on container start.
ENTRYPOINT ["/executedownload.sh"]
