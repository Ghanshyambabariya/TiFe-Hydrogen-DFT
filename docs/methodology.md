# Methodology

## Objective

The computational workflow explores hydrogen incorporation in B2-TiFe using periodic density functional theory and reproducible Python-based structure preparation.

The aim is to connect atomistic modelling with experimental questions in intermetallic hydrogenation, including candidate hydrogen environments, local structural response, and energetic comparison of H-containing configurations.

## Structure Preparation

Ordered B2-TiFe is constructed with Ti at the cube corner and Fe at the body centre. The initial cubic lattice parameter is set to `2.97 angstrom`.

The primitive cell is expanded to a `2 x 2 x 2` supercell for hydrogen insertion, giving a starting composition of `Ti8Fe8`.

## Pristine Relaxation

The pristine cell is prepared for a Quantum ESPRESSO variable-cell relaxation. This allows the lattice parameter, cell volume, and atomic positions to respond to the selected DFT setup.

The input template uses:

- PBE-compatible pseudopotentials
- plane-wave basis
- metallic smearing
- automatic k-point mesh
- spin polarization for the Fe-containing system
- convergence thresholds for the initial workflow

## Convergence Check

The convergence workflow generates inputs for several plane-wave cutoffs and k-point meshes:

- `ecutwfc`: 30, 40, 50, 60 Ry
- k-point meshes: `4x4x4`, `6x6x6`, `8x8x8`

These calculations provide an initial sensitivity check for the numerical parameters before comparing structural or energetic quantities.

## Hydrogen Sites

Three candidate hydrogen positions are generated in the supercell:

- a Ti-rich octahedral-like environment
- a second inequivalent octahedral-like environment
- a tetrahedral-like starting point

Each H-containing structure is intended for structural relaxation before site energies and local environments are compared.

## H2 Reference

An isolated H2 molecule is placed in a large cubic cell and prepared as a reference calculation for evaluating hydrogen incorporation energies.

## Analysis

After Quantum ESPRESSO outputs are available, the analysis extracts or compares:

- total energy
- optimized cell volume
- optimized atomic coordinates
- relative H-site energies
- nearest Ti-H and Fe-H distances
- volume change after hydrogen insertion
- hydrogen incorporation energy using the H2 reference

If the corresponding output files are absent, the result tables retain the status `Calculation pending`.
