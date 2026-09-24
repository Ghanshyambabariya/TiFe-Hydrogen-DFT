# Exploratory DFT Modelling of Hydrogen Incorporation in B2-TiFe

Computational materials workflow for exploring hydrogen incorporation in B2-TiFe intermetallics using Python and Quantum ESPRESSO.

The project builds TiFe crystal structures, generates candidate hydrogen interstitial configurations, prepares Quantum ESPRESSO input files, and provides analysis routines for structural and energetic comparison.

## Research Context

The workflow was developed to complement experimental work on hydrogenation of intermetallic compounds with an atomistic modelling perspective. B2-TiFe is used as a representative system for examining candidate hydrogen environments, local structural changes, and the computational requirements for comparing hydrogen incorporation sites.

## Workflow

- Generate the B2-TiFe primitive cell and a `2 x 2 x 2` Ti8Fe8 supercell.
- Create three candidate H interstitial starting configurations.
- Prepare Quantum ESPRESSO inputs for structural relaxation.
- Generate cutoff and k-point convergence inputs.
- Prepare an H2 reference calculation for hydrogen incorporation-energy analysis.
- Generate optional DOS calculation inputs.
- Analyse local Ti-H/Fe-H distances, cell volume, and energetic outputs.
- Export summary tables and figures.

![DFT workflow overview](figures/dft_workflow_overview.png)

## Current Results

The current repository includes generated structures and geometric pre-screening of the candidate hydrogen sites. Energetic and relaxed-structure quantities are populated after Quantum ESPRESSO outputs are available and parsed.

![Interstitial distance screening](figures/interstitial_distance_screening.png)

See the concise project summary in [docs/showcase.md](docs/showcase.md).

## Quick Start

```powershell
python -m pip install -r requirements.txt
python src/run_workflow_setup.py
```

Example Quantum ESPRESSO execution:

```bash
pw.x < qe_inputs/pristine/TiFe_vc_relax.in > qe_outputs/TiFe_vc_relax.out
```

## Project Layout

```text
structures/   generated CIF and XYZ files
qe_inputs/    Quantum ESPRESSO input templates
src/          Python generation and analysis scripts
results/      CSV summaries
figures/      workflow and analysis figures
docs/         methodology and theory notes
```

## Documentation

- [Methodology](docs/methodology.md)
- [Theory notes](docs/theory_notes.md)
- [Analysis and interpretation](docs/interpretation.md)
