# The Ising model serves as an inspiration to the automaton
# 100 x 100 Ising model. 100,000 Monte Carlo steps
# recording in animation.mp4
# animates only 1% of all steps

from math import exp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit
from numpy import copy, sum, zeros
from random import random


def animate(i):
    im.set_array(spins_record[i])
    return [im]


@njit
def calc_energy(spins):
    n = len(spins)
    energy = 0

    # horizontal pairs
    for i in range(n):
        for j in range(n - 1):
            energy += spins[i][j] * spins[i][j + 1]

    # vertical pairs
    for j in range(n):
        for i in range(n - 1):
            energy += spins[i][j] * spins[i + 1][j]

    return energy


if __name__ == '__main__':
    n = 100
    J = 1
    T = 1
    kB = 1
    mc_steps = 100000

    beta = 1 / (kB * T)
    spins = zeros((n, n))
    spins_record = []
    M_record = zeros(mc_steps)

    record_factor = 1 / 1000
    record_step = int(mc_steps * record_factor)

    for i in range(n):
        for j in range(n):
            spins[i][j] = 1 if random() > 0.5 else -1

    for steps in range(mc_steps):
        rand_i = int(random() * n)
        rand_j = int(random() * n)

        init_energy = -J * calc_energy(spins)
        spins[rand_i][rand_j] *= -1
        final_energy = -J * calc_energy(spins)
        dE = final_energy - init_energy

        if dE <= 0:
            pass
        else:
            if random() < exp(-beta * dE):
                pass
            else:
                spins[rand_i][rand_j] *= -1

        M_record[steps] = sum(spins)

        if steps % record_step == 0:
            print("{:.1f} %".format(steps / mc_steps * 100))
            spins_record.append(copy(spins))

    fig = plt.figure()
    im = plt.imshow(spins_record[0])

    num_frames = len(spins_record)

    animate = FuncAnimation(fig,
                            animate,
                            frames=num_frames,
                            interval=1,
                            repeat=False)
    plt.show()