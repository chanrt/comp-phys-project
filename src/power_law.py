# Averages the final result from an ensemble for simulations
# and plots a log-log graph that conveys power law clustering

from copy import copy
from matplotlib import pyplot as plt
from numpy import around, log, pad, sum, zeros

from cluster import cluster_lattice
from data_manager import load_automaton_data
from linear_regression import perform_linear_regression


def fit_power_law(log_area, log_prob):
    """ Returns power-law exponent, intercept and r_squared for an expected power law distribution """
    beta, c, r_squared = perform_linear_regression(log_area, log_prob)
    return beta, c, r_squared


def get_probabilities(simulation_index, time_step = -1):
    """ Returns an array such that the i^th element is the probability of that any cluster has area greater than or equal to i """
    lattice_record = load_automaton_data(simulation_index)
    final_cluster_sizes = cluster_lattice(lattice_record[time_step], trim=True)
    cumulative_cluster_sizes = copy(final_cluster_sizes[1:])

    for i in range(len(cumulative_cluster_sizes)):
        for j in range(i + 1, len(cumulative_cluster_sizes)):
            cumulative_cluster_sizes[i] += cumulative_cluster_sizes[j]
    probabilities = cumulative_cluster_sizes / sum(final_cluster_sizes[1:])

    return probabilities


def trim_log_probabilities(y):
    """ Trims the last few repetitive elements of log_probabilities """
    last_value = y[-1]

    start_index = -1
    for i in range(len(y)):
        if y[i] == last_value:
            start_index = i
            break

    return y[:start_index + 1]


if __name__ == '__main__':
    # simulations that need to be considered
    simulation_indices = list(range(0, 10))
    ensemble_probabilities = []

    for i, simulation_index in enumerate(simulation_indices):
        print(f"Lattice {i + 1} / {len(simulation_indices)} being processed")
        probabilities = get_probabilities(simulation_index)
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
    print(f"Beta: {beta}")
    print(f"R^2: {r_squared}")

    y_line = -beta * log_areas + c
    plt.title(f"Power law distribution of cluster sizes")
    plt.xlabel("log(a)")
    plt.ylabel("log(P(A >= a))")
    plt.plot(log_areas, log_probabilities, marker="o", linestyle="None", markersize=2)
    plt.plot(log_areas, y_line)
    plt.legend([f"Cluster data from {len(simulation_indices)} simulations", f"Power law fit with beta = {around(beta, 2)}, R^2 = {around(r_squared, 2)}"])
    plt.show()