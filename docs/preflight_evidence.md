# TiFe hydrogen: input quality and calculation plan

## Goals

Catch incorrect Quantum ESPRESSO input files before costly runs, then obtain converged energies for the three existing candidate hydrogen sites.

## Existing evidence

17 input files: 15 pw.x and two dos.x. Seven cutoff/k-point tests, the pristine reference, H2, three hydrogen configurations and DOS inputs are prepared.

A preflight check found a mismatch in H2_scf.in: nspin=1 and one species, but starting_magnetization(1) and starting_magnetization(2) were specified. The generator and input file have been corrected.

The current insertion-energy tables are still pending. No DFT results have been invented, and no hydrogen-site energy ranking is established.

## Workflow

1. Validate input-card structure, atom counts, species counts, cutoffs, k-point meshes and spin initialization.
2. Run and check QE convergence using available pseudopotentials and appropriate hardware.
3. Compare E(Ti8Fe8H) - E(Ti8Fe8) - 0.5 E(H2), with the same computational settings and relaxed structures.

The input audit is not a physics or speed benchmark. Faster error detection may avoid wasted DFT jobs; energy and runtime gains require actual QE measurements.

Sources: https://www.quantum-espresso.org/Doc/INPUT_PW.html and https://www.compmatphys.org/wp-content/uploads/2025/12/2025-12_team02_project-paper.pdf.


## Second check: avoid duplicate starting sites

Site A at (0.25, 0.25, 0) and site B at (0.25, 0, 0.25) differ only by swapping the y and z axes. The script checks that this permutation preserves the atom-resolved Ti and Fe framework in the cubic 2x2x2 cell.

Under those assumptions, the three original starting positions form two distinct groups: {A, B} and {C}. One of three site-relaxation runs could be omitted, a 33.33% reduction in the number of planned H-site calculations. This is a planning result, not measured compute time; symmetry breaking must be checked before applying it to other structures.

[Symmetry audit](../results/preflight/site_symmetry.md) | [Screening script](../src/site_symmetry.py)
