# Interpretation Guidance

## What Can Be Claimed

This project can support the statement:

> I explored whether first-principles modelling could support my experimental work on hydrogenation of intermetallic compounds. Using TiFe as a representative system, I investigated how different hydrogen interstitial environments could be constructed and compared energetically and how hydrogen incorporation could affect the local structure. It was an exploratory component rather than the main focus of the project, but it introduced me to atomistic quantum-mechanical modelling and motivated my interest in more advanced approaches such as QM/MM.

## What Should Not Be Claimed

Do not describe this as:

- a complete DFT study
- a full computational thesis
- a published computational result
- a rigorous hydrogen-storage thermodynamics benchmark
- a QM/MM calculation
- evidence of advanced QM/MM expertise

## Reading Pending Results

If a table says `Calculation pending`, the calculation setup exists but the Quantum ESPRESSO output has not been generated or parsed.

Placeholder plots are included to show the expected analysis products. They are not calculated results.

## Reading Future Calculated Results

When actual outputs are added, site preference should be discussed in terms of:

- relative total energies between relaxed H sites
- nearest Ti-H and Fe-H distances
- local structural distortion
- supercell volume change
- sensitivity to cutoff, k-points, and pseudopotentials

For interview discussion, focus on why the workflow was created and what each calculation would test, rather than overstating numerical precision.
