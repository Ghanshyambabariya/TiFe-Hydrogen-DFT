from build_tife import main as build_tife
from build_supercell import main as build_supercell
from add_hydrogen import main as add_hydrogen
from analyse_structure import main as analyse_structure
from calculate_insertion_energy import main as calculate_insertion
from convergence_analysis import main as convergence
from generate_qe_inputs import main as generate_qe
from plot_results import main as plot_results
from showcase import main as showcase


def main() -> None:
    build_tife()
    build_supercell()
    add_hydrogen()
    generate_qe()
    analyse_structure()
    convergence()
    calculate_insertion()
    plot_results()
    showcase()


if __name__ == "__main__":
    main()
