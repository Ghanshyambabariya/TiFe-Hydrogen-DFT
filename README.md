# Exploratory Quantum-Mechanical Modelling of Hydrogen Incorporation in TiFe Intermetallics

This repository reconstructs an exploratory computational approach investigated during a university research project on hydrogenation of intermetallic compounds. The objective was to understand how basic atomistic and quantum-mechanical calculations could complement experimental investigation of hydrogen-storage materials.

B2-TiFe is used as a representative intermetallic system. The workflow examines pristine TiFe, possible hydrogen interstitial configurations, structural relaxation, hydrogen incorporation energies, and associated structural changes.

The work was exploratory and intended to develop an understanding of first-principles modelling concepts rather than constitute an exhaustive computational study.

## Scientific Question

Which interstitial positions in B2-TiFe are energetically favorable for hydrogen incorporation, and what structural changes occur after hydrogen insertion?

A secondary question is whether simple first-principles calculations can provide qualitative atomic-scale insight that supports experimental understanding of hydrogenation in intermetallic compounds.

## Scope and Scientific Integrity

This repository contains executable calculation templates, structure-generation scripts, parsers, and analysis workflows. It does not contain completed DFT results unless Quantum ESPRESSO output files are explicitly added and parsed.

Values that require DFT execution are marked as `Calculation pending`. No unsupported final numerical results are inserted.

This project should not be read as a full computational thesis, a published DFT campaign, or evidence of advanced QM/MM expertise. It is a small, reproducible exploratory workflow.

## Model System

The starting structure is ordered B2-TiFe, approximately space group `Pm-3m`.

| Atom | Conceptual position | Fractional coordinate |
|---|---|---|
| Ti | cube corner | `(0, 0, 0)` |
| Fe | body centre | `(1/2, 1/2, 1/2)` |

Initial lattice parameter:

```text
a = 2.97 angstrom
```

The workflow then builds a `2 x 2 x 2` supercell with approximate composition `Ti8Fe8` and inserts one H atom into candidate interstitial positions.

## Candidate Hydrogen Sites

The candidate sites are starting configurations for structural relaxation, not pre-assigned final stable sites.

| Site | Description | Fractional coordinate in Ti8Fe8 supercell |
|---|---|---|
| `Site_A_Ti_rich_octahedral` | Ti-rich octahedral-like environment | `(0.25, 0.25, 0.00)` |
| `Site_B_mixed_octahedral` | inequivalent mixed octahedral-like environment | `(0.25, 0.00, 0.25)` |
| `Site_C_tetrahedral_like` | tetrahedral-like starting point | `(0.125, 0.125, 0.125)` |

## Computational Workflow

1. Build primitive B2-TiFe.
2. Generate Quantum ESPRESSO input for pristine variable-cell relaxation.
3. Generate a small convergence-study input set for plane-wave cutoff and k-point mesh.
4. Build a `2 x 2 x 2` TiFe supercell.
5. Insert H into candidate interstitial positions.
6. Generate Quantum ESPRESSO relaxation inputs for each H-containing structure.
7. Parse Quantum ESPRESSO outputs when available.
8. Summarize relative site energies, local Ti-H/Fe-H distances, volume changes, and insertion energies.
9. Optionally run DOS calculations for qualitative electronic-structure comparison.

## Quantum ESPRESSO Setup

The generated inputs use a beginner-level periodic DFT setup:

- PBE-GGA exchange-correlation functional through the selected pseudopotentials
- plane-wave basis
- metallic occupations with smearing
- automatic k-point meshes
- spin polarization for Fe-containing systems
- variable-cell relaxation for pristine TiFe
- fixed-cell atomic relaxation for the initial H-site comparison

Pseudopotentials are referenced by filename in the input templates:

```text
Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
Fe.pbe-spn-kjpaw_psl.1.0.0.UPF
H.pbe-kjpaw_psl.1.0.0.UPF
```

Download suitable open-source pseudopotentials and place them in the working `pseudo` directory used by Quantum ESPRESSO. The exact pseudopotentials should be recorded before interpreting calculated energies.

## Hydrogen Incorporation Energy

The electronic contribution to hydrogen incorporation energy is defined as:

```text
E_insert = E(Ti8Fe8H) - E(Ti8Fe8) - 1/2 E(H2)
```

For quantitative thermodynamics, this value depends on:

- exchange-correlation functional
- pseudopotentials
- cutoff and k-point convergence
- treatment of isolated H2
- zero-point and thermal corrections

This exploratory workflow calculates only the electronic-energy contribution once the required Quantum ESPRESSO outputs exist.

## Relation to Experimental Hydrogenation Work

The computational exploration was motivated by questions arising during the intermetallic-hydrogenation project:

- why hydrogen occupies particular lattice sites
- how local atomic environment affects H stability
- why hydrogenation changes lattice dimensions
- how atomic-scale modelling may support interpretation of experimentally observed hydrogenation behaviour

The computational component was exploratory and supportive. It was used to reason about hydrogen-metal interactions at the atomic level alongside the experimental/research project.

## From Periodic DFT to QM/MM

Periodic DFT treats the complete periodic TiFe model quantum mechanically.

QM/MM instead divides a larger system into a quantum-mechanical region and a molecular-mechanical environment. The TiFe calculation here is not QM/MM.

This project provided introductory exposure to quantum-mechanical atomistic modelling and concepts such as energetic stability, atomic relaxation, local chemical environment, quantum description of bonding, and computational interpretation of experimental materials behaviour. Those concepts are useful foundations for subsequently learning hybrid QM/MM methods.

## Repository Structure

```text
structures/      Generated CIF and XYZ structures
qe_inputs/       Quantum ESPRESSO input templates
src/             Python generation, parsing, and analysis scripts
results/         CSV summaries; pending until QE outputs are parsed
figures/         Generated analysis figures or pending placeholders
docs/            Methodology, theory notes, and interpretation guidance
```

## Quick Start

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Generate structures, Quantum ESPRESSO input templates, pending CSV summaries, and placeholder figures:

```powershell
python src/run_workflow_setup.py
```

Run selected Quantum ESPRESSO inputs manually after installing Quantum ESPRESSO and pseudopotentials. Example:

```bash
pw.x < qe_inputs/pristine/TiFe_vc_relax.in > qe_outputs/TiFe_vc_relax.out
```

Parse an output:

```powershell
python src/parse_qe_output.py qe_outputs/TiFe_vc_relax.out --json parsed_outputs/TiFe_vc_relax.json
```

Re-run the analysis scripts after parsed outputs are available.

## Current Status

The repository currently provides setup, reproducible input generation, parser scaffolding, pending result tables, and plotting templates.

DFT calculation outputs are not included. Result tables intentionally show `Calculation pending` where Quantum ESPRESSO calculations have not yet been run.
