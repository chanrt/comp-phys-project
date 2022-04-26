# Simulates the vegetation automaton
# Shows animation
# Saves data in automaton_data

from concurrent.futures import ThreadPoolExecutor
from itertools import product
from math import sqrt
from numba import njit
from numpy import copy, sum, zeros
from matplotlib import pyplot as plt
from random import random

from file_manager import save_automaton_data


@njit(fastmath=True, nogil=False)
def mc_step(lattice):
    """ Simulates a single Monte Carlo step of the automaton """
    n = len(lattice)
    f_current = sum(lattice) / (n * n)
    num_updates = int(mc_fraction * n * n)

    for _ in range(num_updates):
        i = int(random() * n)
        j = int(random() * n)
        rho = get_density(lattice, i, j)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
        else:
            prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0


@njit(fastmath=True, nogil=False)
def get_density(lattice, i, j):
    """ Calculates the vegetation density in the neighbourhood of a given cell (i, j) """
    n = len(lattice)
    normalization = 0
    density = 0

    for a in range(i - r_influence, i + r_influence + 1):
        for b in range(j - r_influence, j + r_influence + 1):
            if 0 < a < n and 0 < b < n and (i - a) ** 2 + (j - b) ** 2 < r_influence ** 2:
                weightage_term = 1 - get_distance(i, j, a, b) / immediacy
                density += weightage_term * lattice[a, b]
                normalization += weightage_term
    return density / normalization


@njit
def get_distance(i, j, a, b):
    """ Calculates the distance between two cells at locations (i, j) and (a, b) """
    return sqrt((i - a)**2 + (j - b)**2)


def make_initial_lattice(n):
    """ Generates a random initial lattice with occupancy around 50% """
    lattice = zeros((n, n), dtype=int)
    for i, j in product(range(n), range(n)):
        lattice[i, j] = 1 if random() > 0.5 else 0
    return lattice


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702
    return slope * rainfall + intercept


def simulate(simulation_index):
    lattice = make_initial_lattice(n)
    lattice_record = []

    for step in range(mc_steps):
        if simulation_index == num_simulations - 1:
            print(f"{round(step * 100 /mc_steps, 2)} %", end="\r")
        mc_step(lattice)
        lattice_record.append(copy(lattice))

    return lattice_record


if __name__ == '__main__':
    show_trajectory = False

    # simulation parameters
    mc_steps = 200
    mc_fraction = 0.2

    # constants
    n = 500
    rainfall = 500
    f_carrying = get_forest_cover(rainfall)
    r_influence = 5
    immediacy = 24

    num_simulations = 5

    with ThreadPoolExecutor(num_simulations) as pool:
        lattice_records = pool.map(simulate, range(num_simulations))

    for lattice_record in lattice_records:
        save_automaton_data(lattice_record)

        if show_trajectory:
            time = list(range(mc_steps))
            forest_cover = [sum(lattice) / (n * n) for lattice in lattice_record]
            plt.title(f"Change of forest cover with time (rainfall = {rainfall} mm/year)")
            plt.xlabel("Time (years)")
            plt.ylabel("Forest cover")
            plt.plot(time, forest_cover)
            plt.plot(time, [f_carrying] * len(time))
            plt.legend(["Forest cover", "Carrying capacity"])
            plt.show()
        