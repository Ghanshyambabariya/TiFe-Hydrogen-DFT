# Theory Notes

## Density Functional Theory

Density Functional Theory is a quantum-mechanical method for estimating the electronic structure and total energy of atoms, molecules, and solids. Instead of solving directly for the full many-electron wavefunction, DFT uses the electron density as the central variable.

## Exchange-Correlation Functional

The exchange-correlation functional approximates electron exchange and correlation effects. This workflow assumes a PBE-GGA style setup through the chosen pseudopotentials. Different functionals can shift relative energies and structural parameters.

## Plane-Wave Basis

Plane-wave DFT represents electronic wavefunctions using waves compatible with periodic boundary conditions. The plane-wave cutoff controls how many basis functions are included. Higher cutoffs are usually more accurate but more expensive.

## Pseudopotentials

Pseudopotentials replace the chemically inert core electrons with an effective potential. This reduces computational cost while retaining the valence-electron behaviour important for bonding.

## Periodic Boundary Conditions

Periodic boundary conditions repeat the simulation cell infinitely in all directions. They are natural for crystalline solids such as B2-TiFe.

## Structural Relaxation

Structural relaxation adjusts atomic coordinates and sometimes the cell shape/volume to reduce forces and stress. Relaxed structures are needed before comparing local bonding or relative energies.

## k-Point Sampling

k-points sample the Brillouin zone of a periodic material. Metals and small unit cells often require careful k-point convergence because electronic states near the Fermi level affect total energy.

## Hydrogen Interstitial Sites

An interstitial site is a position in the crystal lattice not normally occupied by host atoms. Hydrogen can occupy interstitial environments in metals and intermetallics, and its stability depends on local coordination and electronic structure.

## Hydrogen Incorporation Energy

Hydrogen incorporation energy compares the energy of hydrogen inside the metal lattice with the pristine metal and an H2 reference. It is useful for comparing candidate sites, but quantitative interpretation requires careful convergence and thermodynamic corrections.

## Density of States

The density of states describes how electronic states are distributed with energy. Comparing TiFe and TiFe + H DOS can give qualitative insight into electronic changes after hydrogen incorporation. It should not be overinterpreted without careful calculation settings.

## DFT, Molecular Mechanics, and QM/MM

DFT treats electrons quantum mechanically and can describe bonding changes. Molecular mechanics uses classical force fields and is usually cheaper but less electronic-detail rich. QM/MM combines a quantum-mechanical region with a molecular-mechanical environment. This TiFe workflow is periodic DFT, not QM/MM.
