# Methodology

## Objective

The computational workflow explores whether basic periodic DFT calculations can provide qualitative atomic-scale insight into hydrogen incorporation in B2-TiFe.

The aim is not to produce a definitive DFT benchmark. The aim is to build a transparent, reproducible setup that can be discussed alongside experimental hydrogenation work.

## Structure Preparation

Ordered B2-TiFe is constructed with Ti at the cube corner and Fe at the body centre. The initial cubic lattice parameter is set to `2.97 angstrom`.

The primitive cell is expanded to a `2 x 2 x 2` supercell for hydrogen insertion. This gives a starting composition of `Ti8Fe8`.

## Pristine Relaxation

The pristine cell is prepared for a Quantum ESPRESSO variable-cell relaxation. This allows the lattice parameter, cell volume, and atomic positions to respond to the selected DFT setup.

The input template uses:

- PBE-compatible pseudopotentials
- plane-wave basis
- metallic smearing
- automatic k-point mesh
- spin polarization for the Fe-containing system
- convergence thresholds suitable for an exploratory calculation

## Convergence Check

The convergence workflow generates inputs for several plane-wave cutoffs and k-point meshes:

- `ecutwfc`: 30, 40, 50, 60 Ry
- k-point meshes: `4x4x4`, `6x6x6`, `8x8x8`

The purpose is to show awareness that DFT results depend on numerical parameters. This is not presented as a rigorous convergence publication.

## Hydrogen Sites

Three candidate hydrogen positions are generated in the supercell:

- a Ti-rich octahedral-like environment
- a second inequivalent octahedral-like environment
- a tetrahedral-like starting point

Each H-containing structure is intended for structural relaxation before interpreting site preference.

## Analysis

After Quantum ESPRESSO outputs are available, the analysis should extract:

- total energy
- optimized cell volume
- optimized atomic coordinates
- relative H-site energies
- nearest Ti-H and Fe-H distances
- volume change after hydrogen insertion
- hydrogen incorporation energy using an H2 reference

If output files are absent, tables remain marked as `Calculation pending`.
