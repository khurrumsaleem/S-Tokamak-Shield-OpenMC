#!/bin/bash
# =============================================================================
# executedownload.sh
# Runs every time the container starts.
# Downloads nuclear data on first run only, then starts JupyterLab.
# =============================================================================
set -e

NUCLEAR_DATA_DIR="/nuclear_data"
CROSS_SECTIONS="$NUCLEAR_DATA_DIR/cross_sections.xml"

# Only download if cross_sections.xml is not already present
if [ ! -f "$CROSS_SECTIONS" ]; then
    echo "============================================"
    echo "  Nuclear data not found — downloading..."
    echo "  This only happens ONCE"
    echo "============================================"
    mkdir -p /nuclear_data

    # ── Step 1: Depletion chain ───────────────────────────────────────────────
    echo "Step 1/4 — Downloading depletion chain..."
    download_chain \
        -l endf \
        -r b8.0 \
        -b SFR \
        -d /nuclear_data/ \
        -f chain-endf-b8.0.xml

    # ── Step 2: ENDF/B-VIII.0 cross sections ─────────────────────────────────
    echo "Step 2/4 — Downloading ENDF/B-VIII.0 cross sections (~2 GB)..."
    echo "          Terminal will look frozen during extraction — please wait."
    wget -q -O - \
        https://anl.box.com/shared/static/uhbxlrx7hvxqw27psymfbhi7bx7s6u6a.xz \
        | tar -C /nuclear_data -xJ

    # ── Step 3: Flatten directory structure ───────────────────────────────────
    echo "Step 3/4 — Reorganising folder structure..."
    mv /nuclear_data/endfb-viii.0-hdf5/* /nuclear_data/
    rm -rf /nuclear_data/endfb-viii.0-hdf5

    # ── Step 4: Windowed Multipole library ────────────────────────────────────
    echo "Step 4/4 — Downloading Windowed Multipole library..."
    wget https://github.com/mit-crpg/WMP_Library/releases/download/v1.1/WMP_Library_v1.1.tar.gz \
        -O /nuclear_data/WMP_Library_v1.1.tar.gz
    tar -xzf /nuclear_data/WMP_Library_v1.1.tar.gz -C /nuclear_data
    rm /nuclear_data/WMP_Library_v1.1.tar.gz

    echo "============================================"
    echo "  All nuclear data ready."
    echo "============================================"
else
    echo "Nuclear data already present — skipping download."
fi

# Point OpenMC to cross_sections.xml
export OPENMC_CROSS_SECTIONS=/nuclear_data/cross_sections.xml

# Start JupyterLab -- ip/port/token/notebook_dir/allow_root are all set in
# /root/.jupyter/jupyter_lab_config.py (baked in at build time), so no CLI
# flags are needed here, same as in openmc-prism.
echo "Starting JupyterLab at http://localhost:8888 ..."
exec jupyter lab
