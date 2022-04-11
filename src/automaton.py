# Simulates the vegetation automaton
# Shows animation

from itertools import product
from numba import njit
from numpy import copy, sum, zeros
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from pickle import dump
from random import random


@njit(fastmath=True, nogil=False)
def mc_step(lattice):
    n = len(lattice)
    f_current = sum(lattice) / (n * n)

    num_updates = int(mc_fraction * n * n)

    for _ in range(num_updates):
        i = int(random() * n)
        j = int(random() * n)
        rho = get_rho(lattice, i, j)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
        else:
            prob_decay = rho + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0
    return lattice


@njit(fastmath=True, nogil=False)
def get_rho(lattice, i, j):
    n = len(lattice)
    s = 0
    rho = 0

    for a in range(i - r_influence, i + r_influence + 1):
        for b in range(j - r_influence, j + r_influence + 1):
            if 0 < a < n and 0 < b < n and (i - a) ** 2 + (j - b) ** 2 < r_influence ** 2:
                rho += lattice[a, b]
                s += 1
    return rho / s


def make_initial_lattice(n):
    lattice = zeros((n, n), dtype=int)
    for i, j in product(range(n), range(n)):
        lattice[i, j] = 1 if random() > 0.5 else 0
    return lattice


def get_forest_cover(rainfall):
    # this fit was done in linear_regression.py
    slope = 0.0008588
    intercept = -0.1702
    return slope * rainfall + intercept


def save_data(lattice_record):
    num_files = len([name for name in os.listdir(os.path.join(os.path.dirname(__file__), 'automaton_data'))])
    file_name = 'simulation_{}.pkl'.format(num_files)
    path_name = os.path.join(os.path.dirname(__file__), 'automaton_data', file_name)
    dump(lattice_record, open(path_name, 'wb'))


def animate(i):
    im.set_array(lattice_record[i])
    return [im]


if __name__ == '__main__':
    n = 500  # dimensions of lattice
    mc_steps = 200  # in years
    mc_fraction = 0.2  # 20% of the cells are updated in every step
    rainfall = 500  # in mm
    f_carrying = get_forest_cover(rainfall)
    r_influence = 4  # radius of influence

    lattice = make_initial_lattice(n)
    lattice_record = []

    print("Compiling functions (will take a few seconds) ...")
    for step in range(mc_steps):
        print(f"Year {step}")
        mc_step(lattice)
        lattice_record.append(copy(lattice))

    save_data(lattice_record)
    fig = plt.figure()
    im = plt.imshow(lattice_record[0])

    num_frames = len(lattice_record)

    animate = FuncAnimation(fig,
                            animate,
                            frames=num_frames,
                            interval=10,
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