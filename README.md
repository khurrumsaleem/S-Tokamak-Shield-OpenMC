# NEUTRONICS ANALYSIS TO OPTIMISE NEUTRON SHIELDING MATERIALS IN SPHERICAL TOKAMAK USING OPENMC

## Introduction

Compact, high-field spherical tokamaks leave very little space around the central column — yet the superconducting magnets housed there are highly sensitive to nuclear heating and radiation-induced damage. The central column shield exists to solve exactly this: it limits activation of components outside the shield (so maintenance stays practical) and protects the magnets and structural elements from radiation damage and excessive heating that would otherwise compromise the cryogenic system.

This project uses OpenMC to find shielding materials that minimise energy deposition and radiation damage in the central-column magnet of a spherical tokamak, without exceeding its tight radial space budget. A parametric tokamak model (plasma, first wall, breeder blanket, and a swappable central-column shield) is built in CAD, converted to DAGMC geometry, and irradiated with a 14 MeV neutron source in OpenMC. Candidate materials — from conventional moderators, absorbers, and attenuators (water, boron carbide, lead, steel) to exotic compounds such as tungsten boride — are screened against two figures of merit: **nuclear heating (W/g)** and **radiation damage (eV per source particle)** in the magnet.

**Tungsten boride** came out on top, cutting energy deposition to **0.0002253 W/g** and radiation damage to **42.703 eV per source particle** — outperforming every traditional moderator/absorber/attenuator tested. Exotic, multifunctional materials look like the more promising direction for space-constrained shielding, though a wider sweep of materials and geometries is still needed to generalise this result. The whole pipeline is packaged as a one-command Docker environment so it can be rerun or extended without rebuilding the toolchain by hand.

---

## Architecture

The notebook runs as four phases, each one feeding the next:

```
 Phase A — Geometry Build (paramak + CadQuery)
   Parametrise plasma, blanket, first wall, central-column shield
   -> generate CAD solids -> mesh via gmsh -> export DAGMC .h5m
               |
               ▼
 Phase B — Materials & Source
   Select candidate material (water / B4C / lead / steel / WB2, ...)
   from materials.py -> build openmc.Materials
   Define 14 MeV neutron source (optionally via openmc_plasma_source)
               |
               ▼
 Phase C — Model Assembly
   Combine DAGMC geometry + materials + source + tallies
   -> single openmc.Model, ready to run
               |
               ▼
 Phase D — Transport & Post-Processing
   Run OpenMC (DAGMC-enabled) -> statepoint.h5
   Convert tallies eV -> W/g (openmc_tally_unit_converter)
   Plot geometry / source / mesh tallies -> compare candidate materials
               |
               ▼
   Swap the material in Phase B and repeat C-D for the next candidate.
```

Materials are the only thing that changes between runs — geometry (Phase A) and the transport setup (Phases C-D) stay fixed, so each candidate shield material is a like-for-like comparison.

---

## Why paramak?

- Hand-building curved tokamak surfaces in OpenMC's native CSG is slow and fragile.
- [Paramak](https://github.com/fusion-energy/paramak) generates geometry (`spherical_tokamak`, `center_column_shield_cylinder`, `blanket_from_plasma`, `plasma_simplified`, …) from a few physical parameters instead.
- Built on real CAD (CadQuery), feeds straight into the DAGMC meshing toolchain.
- Makes it easy to sweep shield thickness/material with no manual redrawing.
- Uses the current function-based API (`>=0.9.8`), not the older class-based `Reactor` API (0.8.x).

## How materials are defined

- All materials are defined in `notebooks/materials.py`.
- Fixed materials (plasma, tungsten blanket, copper magnet, stainless steel tie bar) are built directly as `openmc.Material` objects.
- ~24 candidate central-column shield materials (water, B₄C, lead, steel, tungsten boride, etc.) are stored as plain density + nuclide/element weight-fraction dictionaries.
- Helper functions (`build_inshield_material`, `build_all_materials`, `export_material_xml_files`) assemble these into `openmc.Materials` and export per-candidate XML — runnable standalone via `python materials.py`.

## How the Docker image is built

- Base: `ubuntu:24.04` (native Python 3.12).
- OpenMC + MOAB: prebuilt, DAGMC-enabled wheels from Jonathan Shimwell's wheel index — no source compile.
- Everything else: installed from PyPI.
- Nuclear data: excluded from the image; fetched once at container start by `executedownload.sh` into a mounted `/nuclear_data` volume.
- JupyterLab then launches automatically.

---

## Installation & Usage

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running.
- ~2 GB of free disk space for the nuclear data download (downloaded once, then cached on the host).

### 1. Pull the image

```bash
docker pull ghcr.io/light0vij/s-tokamak-shield-openmc:latest
```

### 2. Run the container

```bash
docker run -p 8888:8888 -v /YOUR_FOLDER_PATH:/nuclear_data ghcr.io/light0vij/s-tokamak-shield-openmc:latest
```

Replace `/YOUR_FOLDER_PATH` with a folder on your host machine. This is mounted to `/nuclear_data` inside the container so that:
- the ~2 GB nuclear data download (ENDF/B-VIII.0 cross sections, depletion chain, WMP library) only happens **once**, and
- the data persists across container restarts/re-runs instead of being re-downloaded every time.

On first start, `executedownload.sh` will download and unpack the nuclear data (this can take several minutes), then start JupyterLab. On subsequent runs against the same mounted folder, the download step is skipped automatically.

### 3. Open JupyterLab

Once the log shows `Starting JupyterLab at http://localhost:8888 ...`, open:

```
http://localhost:8888
```

No token or password is required (configured for local/offline use — avoid exposing port 8888 on an untrusted network).

### Optional: persist notebooks/outputs too

To also keep notebook edits and generated outputs outside the container:

```bash
docker run -p 8888:8888 \
  -v /YOUR_FOLDER_PATH:/nuclear_data \
  -v /YOUR_NOTEBOOKS_PATH:/home/neutronics/notebooks \
  ghcr.io/light0vij/s-tokamak-shield-openmc:latest
```

---

## Repository structure

```
S-Tokamak-Shield-OpenMC/
├── Dockerfile              # Image build (Ubuntu 24.04 + shimwell OpenMC/MOAB wheels)
├── docker-compose.yml       # Convenience compose file for the volume-mounted run above
├── executedownload.sh       # Container entrypoint: one-time nuclear data fetch + JupyterLab launch
├── requirements.txt          # Pinned/curated Python dependency set (paramak, cad_to_dagmc, etc.)
├── notebooks/                # Analysis notebook(s) + materials.py (material definitions)
└── .github/workflows/        # CI: builds and publishes the image to GHCR
```

---

## Key dependencies

| Package | Role |
|---|---|
| `openmc` (DAGMC build) | Monte Carlo neutron/photon transport engine |
| `paramak` | Parametric fusion-reactor CAD geometry |
| `cadquery` | CAD kernel used by paramak |
| `cad_to_dagmc` | Meshes CAD assemblies into DAGMC `.h5m` geometry |
| `moab` (pymoab) | Mesh-based geometry representation used by DAGMC |
| `materials.py` (in `notebooks/`) | Candidate shield + fixed material definitions → `openmc.Material` |
| `openmc_plasma_source` | Realistic fusion plasma neutron source |
| `openmc_tally_unit_converter` | Converts raw tallies (eV) into physical units (W/g) |
| `openmc_regular_mesh_plotter`, `openmc_source_plotter`, `openmc_depletion_plotter` | Visualisation of mesh tallies, source, and depletion results |
| `gmsh` | Meshing backend used internally by `cad_to_dagmc` |

---

## Results summary

Across the screened shielding candidates (conventional moderators, absorbers, and attenuators vs. exotic compounds), **tungsten boride** was the standout performer for protecting the central-column magnet, achieving:

- **Energy deposition (nuclear heating):** 0.0002253 W/g
- **Radiation damage:** 42.703 eV per source particle

These results suggest that exotic, multifunctional shielding compounds can outperform traditional single-purpose moderators/absorbers/attenuators in the tightly space-constrained shielding geometry of a spherical tokamak — though further work across a broader materials and geometry space is needed to generalise these conclusions.

---

## Acknowledgements & Reference

This environment recreates the toolchain and conventions established by [`fusion-energy/neutronics-workshop`](https://github.com/fusion-energy/neutronics-workshop) and relies heavily on the open-source [OpenMC](https://openmc.org/), [paramak](https://github.com/fusion-energy/paramak), and DAGMC/MOAB ecosystems maintained by Jonathan Shimwell and the wider fusion-energy community.


Romano, P. K., Horelik, N. E., Herman, B. R., Nelson, A. G., Forget, B., & Smith, K. (2015). OpenMC: A State-of-the-Art Monte Carlo Code for Research and Development. Annals of Nuclear Energy, 82, 90–97. https://doi.org/10.1016/j.anucene.2014.07.048


