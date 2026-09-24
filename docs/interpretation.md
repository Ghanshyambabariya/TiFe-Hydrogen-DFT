# Analysis and Interpretation

## Geometric Pre-Screening

The generated H-containing structures provide starting configurations for relaxation. Distances measured from these unrelaxed structures are useful for comparing the local coordination environments of the candidate sites.

These geometric values should be interpreted as initial descriptors rather than relaxed structural properties.

## Energetic Comparison

After Quantum ESPRESSO calculations are available, candidate hydrogen sites can be compared using:

- relaxed total energies
- relative site energies
- hydrogen incorporation energies using an H2 reference
- sensitivity to plane-wave cutoff and k-point sampling

The hydrogen incorporation energy is evaluated from the calculated energies of Ti8Fe8H, pristine Ti8Fe8, and H2.

## Local Structural Analysis

For each relaxed H-containing structure, the analysis can examine:

- nearest Ti-H distances
- nearest Fe-H distances
- changes in local coordination
- atomic displacements around H
- supercell volume change

These descriptors help connect energetic differences with the local atomic environment.

## Electronic Structure

Optional DOS calculations are included for qualitative comparison of the electronic structure before and after hydrogen incorporation.

Relevant features include:

- changes near the Fermi level
- redistribution of states after H insertion
- differences between pristine and H-containing structures

## Numerical Sensitivity

Interpretation of calculated energies should consider:

- plane-wave cutoff
- k-point mesh
- pseudopotential choice
- smearing parameters
- structural-relaxation convergence

The repository includes input sets for initial cutoff and k-point sensitivity checks.

## Current Data Status

Where Quantum ESPRESSO outputs are not yet available, corresponding result fields remain marked `Calculation pending`. Once output files are added, the analysis scripts can populate the energetic and relaxed-structure quantities.
