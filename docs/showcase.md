# Project Showcase

This page summarizes the structures, workflow components, and geometric pre-screening currently included in the repository.

## Generated Workflow Components

- B2-TiFe primitive structure generated from explicit fractional positions.
- `2 x 2 x 2` Ti8Fe8 supercell generated reproducibly.
- Three candidate H interstitial starting structures created as CIF/XYZ files.
- Quantum ESPRESSO input templates for pristine relaxation, convergence checks, H-site relaxation, H2 reference, and optional DOS.
- Python routines for structure generation, output parsing, tabulation, and plotting.
- CSV result tables prepared for calculated outputs.

![DFT workflow overview](../figures/dft_workflow_overview.png)

## Geometric Pre-Screening

The table below reports distances from the generated, unrelaxed starting geometries.

| Site | Fractional H start | nearest Ti-H (A) | nearest Fe-H (A) | Status |
|---|---:|---:|---:|---|
| `Site_A_Ti_rich_octahedral` | `(0.250, 0.250, 0.000)` | `2.100` | `1.485` | Calculation pending |
| `Site_B_mixed_octahedral` | `(0.250, 0.000, 0.250)` | `2.100` | `1.485` | Calculation pending |
| `Site_C_tetrahedral_like` | `(0.125, 0.125, 0.125)` | `1.286` | `1.286` | Calculation pending |

![Interstitial distance screening](../figures/interstitial_distance_screening.png)

## Quantities Populated After QE Execution

After the corresponding Quantum ESPRESSO calculations are run and parsed, the workflow can populate:

- optimized lattice parameter
- final total energies
- relative H-site energies
- hydrogen incorporation energies
- relaxed volume change
- DOS comparison
- relaxed Ti-H and Fe-H distances

The analysis scripts are structured so these quantities can be added directly from calculation outputs.
