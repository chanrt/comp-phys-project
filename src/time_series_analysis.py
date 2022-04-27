from matplotlib import pyplot as plt
from numpy import log, pad, zeros

from power_law import fit_power_law, get_probabilities, trim_log_probabilities

if __name__ == '__main__':
    # simulations to be considered from automaton_data
    simulation_indices = list(range(0, 10))

    # times at which the lattice will be sampled for clustering
    time_indices = list(range(0, 200, 10))

    beta_time_series = []
    r_squared_time_series = []

    for i, time in enumerate(time_indices):
        print(f"At time step {i + 1} / {len(time_indices)}:")

        ensemble_probabilities = []

        for i, simulation_index in enumerate(simulation_indices):
            print(f"    Lattice {i + 1} / {len(simulation_indices)} being processed")
            probabilities = get_probabilities(simulation_index, time)
            ensemble_probabilities.append(probabilities)

        max_length = max([len(probabilities) for probabilities in ensemble_probabilities])
        averaged_probability = zeros(max_length, dtype=float)

        for probabilities in ensemble_probabilities:
            padded_probabilities = pad(probabilities, (0, max_length - len(probabilities)), mode="constant", constant_values=0)
            averaged_probability += padded_probabilities

        averaged_probability /= len(ensemble_probabilities)

        log_probabilities = trim_log_probabilities(log(probabilities))
        log_areas = log(range(1, len(log_probabilities) + 1))

        beta, c, r_squared = fit_power_law(log_areas, log_probabilities)
        beta *= -1
        
        beta_time_series.append(beta)
        r_squared_time_series.append(r_squared)

    plt.title("Variation of power-law exponent with time")
    plt.xlabel("Time")
    plt.ylabel("Power-law exponent")
    plt.plot(time_indices, beta_time_series)
    plt.show()

    plt.title("Variation of R-squared with time")
    plt.xlabel("Time")
    plt.ylabel("R-squared")
    plt.plot(time_indices, r_squared_time_series)
    plt.show()