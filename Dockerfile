# =============================================================================
# Dockerfile
#
# Recreates the fusion-energy/neutronics-workshop (ghcr.io/fusion-energy/
# neutronics-workshop) environment for the Spherical Tokamak shielding
# study (vvij_ptnr_2023.ipynb) — WITHOUT compiling OpenMC/MOAB/DAGMC/
# Embree/Double-Down from source.
#
# OpenMC (with DAGMC support) and MOAB (pymoab) are installed from
# Jonathan Shimwell's community wheel index, exactly as the workshop's own
# tooling recommends:
#
#   pip install --extra-index-url https://shimwell.github.io/wheels openmc
#
# Those wheels are built for CPython 3.12 on manylinux_2_28, so this image
# is pinned to Python 3.12 on a Debian bookworm-based base (glibc-compatible
# with manylinux_2_28). CadQuery (paramak's CAD backend) has its own
# official PyPI wheels since v2.4, so no conda/conda-forge step is needed
# at all -- the whole image is built with plain pip.
#
# Nuclear data (ENDF/B-VIII.0 cross sections + WMP library) is intentionally
# NOT baked into this image, to keep it small. It is downloaded separately,
# on first container start, by executedownload.sh — see that file and the
# README for details.
#
# Build:
#   docker build -t tokamak-neutronics .
#
# Run (mount a host folder for nuclear_data so the ~2GB download only
# happens once, and a folder for your notebooks/outputs):
#   docker run -p 8888:8888 \
#       -v $PWD/nuclear_data:/nuclear_data \
#       -v $PWD/notebooks:/home/neutronics/notebooks \
#       tokamak-neutronics
# =================================================================================

FROM ubuntu:24.04

LABEL maintainer="light0vij" \
      description="NEUTRONICS ANALYSIS TO OPTIMISE NEUTRON SHIELDING MATERIALS IN SPHERICAL TOKAMAK USING OPENMC (+ DAGMC + Paramak), based on fusion-energy/neutronics-workshop, using shimwell's DAGMC-enabled OpenMC/MOAB wheels"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1

# ------------------------------------------------------------------------------------
# System dependencies
#   - python3.12 + venv/pip: Ubuntu 24.04 (noble) ships Python 3.12 natively,
#     matching the CPython version the shimwell wheels (openmc/moab)
#   - OpenGL / Mesa / X libs: needed for CadQuery / paramak / gmsh headless
#     geometry rendering and SVG/STL export.
#   - libhdf5: OpenMC's statepoint/summary files are HDF5.
#   - git/wget/curl: used by the nuclear-data download step and some pip
#     packages that fetch resources at install time.
# ------------------------------------------------------------------------------------------
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        python3.12 \
        python3-pip \
        python3.12-venv \
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
    ln -sf /usr/bin/python3.12 /usr/local/bin/python && \
    ln -sf /usr/bin/python3.12 /usr/local/bin/python3

WORKDIR /home/neutronics

# ********************************************************************
# Python (pip / wheel) dependencies
#   openmc + moab are pulled from shimwell's DAGMC-enabled wheel index
#   (declared via --extra-index-url inside requirements.txt itself);
#   everything else resolves from normal PyPI.
# ********************************************************************-
#COPY requirements.txt /home/neutronics/requirements.txt
#RUN pip install --upgrade pip && \  ––––––––––––––––––> upgrade not allowed while building - so deleting it
RUN pip install --no-cache-dir -r /home/neutronics/requirements.txt


# Project files
COPY materials.py /home/neutronics/materials.py
COPY notebooks/ /home/neutronics/notebooks/
#COPY executedownload.sh /home/neutronics/executedownload.sh
RUN chmod +x /home/neutronics/executedownload.sh

# Nuclear data lives outside the image (downloaded on first run into this
# mount point) to keep the image lean.
ENV OPENMC_CROSS_SECTIONS=/nuclear_data/cross_sections.xml \
    OPENMC_CHAIN_FILE=/nuclear_data/chain-endf-b8.0.xml
RUN mkdir -p /nuclear_data

EXPOSE 8888

# executedownload.sh downloads the nuclear data (once) then launches
# JupyterLab on container start.
ENTRYPOINT ["/home/neutronics/executedownload.sh"]
