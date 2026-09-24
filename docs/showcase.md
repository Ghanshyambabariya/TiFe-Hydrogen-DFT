# Project Showcase

This page summarizes what the repository can currently demonstrate without pretending that full Quantum ESPRESSO calculations have already been completed.

## Current Demonstrable Outputs

- B2-TiFe primitive structure generated from explicit fractional positions.
- `2 x 2 x 2` Ti8Fe8 supercell generated reproducibly.
- Three candidate H interstitial starting structures created as CIF/XYZ files.
- Quantum ESPRESSO input templates for pristine relaxation, convergence checks, H-site relaxation, H2 reference, and optional DOS.
- Parser and analysis scripts prepared for real QE outputs.
- Result CSVs intentionally marked `Calculation pending` where DFT execution is still required.

![DFT workflow overview](../figures/dft_workflow_overview.png)

## Geometric Pre-Screening

The table below reports distances from the generated, unrelaxed starting geometries. These values are useful for explaining the candidate-site construction, but they are not DFT stability results.

| Site | Fractional H start | nearest Ti-H (A) | nearest Fe-H (A) | Status |
|---|---:|---:|---:|---|
| `Site_A_Ti_rich_octahedral` | `(0.250, 0.250, 0.000)` | `2.100` | `1.485` | Calculation pending |
| `Site_B_mixed_octahedral` | `(0.250, 0.000, 0.250)` | `2.100` | `1.485` | Calculation pending |
| `Site_C_tetrahedral_like` | `(0.125, 0.125, 0.125)` | `1.286` | `1.286` | Calculation pending |

![Interstitial distance screening](../figures/interstitial_distance_screening.png)

## What Requires Quantum ESPRESSO Execution

The following outputs cannot be claimed until the corresponding QE calculations are run and parsed:

- optimized lattice parameter
- final total energies
- relative H-site energies
- hydrogen insertion energies
- relaxed volume change
- DOS and projected DOS interpretation

## Best Interview Framing

This project is best presented as a careful exploratory workflow: structure construction, first-principles input preparation, convergence awareness, and analysis scaffolding for hydrogen incorporation in TiFe. The scientifically honest result at this stage is that the computational framework is ready, while full energetic conclusions are pending actual DFT execution.
