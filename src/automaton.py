# Simulates the vegetation automaton
# Shows animation
# Saves data in automaton_data

from itertools import product
from math import sqrt
from numba import njit
from numpy import array, copy, sum, zeros
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from pickle import dump
from random import random


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
                weightage_term = 1 - get_distance(i, j, a, b) / k
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


def save_automaton_data(lattice_record):
    """ Saves the entire simulation data in a pickle file under automaton_data """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(os.path.join(current_path, "automaton_data"))

    num_automaton_simulations = 0
    for file_name in files_list:
        if file_name.startswith("simulation_") and file_name.endswith(".pkl"):
            num_automaton_simulations += 1

    file_name = 'simulation_{}.pkl'.format(num_automaton_simulations)
    path_name = os.path.join(current_path, 'automaton_data', file_name)
    dump(array(lattice_record, dtype=bool), open(path_name, 'wb'))


def animate(i):
    """" Animates a given frame (i) of the simulation """
    im.set_array(lattice_record[i])
    return [im]


if __name__ == '__main__':
    #############
    # CONSTANTS #
    #############
    n = 500  # dimensions of lattice
    mc_steps = 200  # in years
    mc_fraction = 0.2  # 20% of the cells are updated in every step
    rainfall = 500  # in mm
    f_carrying = get_forest_cover(rainfall)
    r_influence = 5  # radius of influence
    k = 24  # measure of decrease in weightage of neighbours

    ###########
    # LATTICE #
    ###########
    lattice = make_initial_lattice(n)
    lattice_record = []

    ##############
    # SIMULATION #
    ##############
    print("Compiling functions (will take a few seconds) ...")
    for step in range(mc_steps):
        print(f"Year {step}")
        mc_step(lattice)
        lattice_record.append(copy(lattice))

    save_automaton_data(lattice_record)

    #############
    # ANIMATION #
    #############
    fig = plt.figure()
    im = plt.imshow(lattice_record[0])
    num_frames = len(lattice_record)
    animate = FuncAnimation(fig,
                            animate,
                            frames=num_frames,
                            interval=50,
                            repeat=False)
    plt.show()

    forest_cover = [sum(lattice) / (n * n) for lattice in lattice_record]
    plt.title("Change of forest cover with time")
    plt.xlabel("Time (years)")
    plt.ylabel("Forest cover")
    plt.plot(range(num_frames), forest_cover)
    plt.plot(range(num_frames), [f_carrying] * num_frames)
    plt.legend(["Forest cover", "Carrying capacity"])
    plt.show()