# Goes through every saved data file from automaton_data
# Generates a time series data of number of clusters of each size, for every year

from matplotlib import pyplot as plt
from numpy import array, zeros
from pickle import dump, load
import os


def cluster(lattice):
    """ Calculates number of clusters of each size, in the given lattce """
    n = len(lattice)
    cluster_sizes = zeros((n * n + 1), dtype=(int))
    visited = zeros((n, n), dtype=(int, int))

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                visited[i][j] = 1

                if lattice[i][j] == 0:
                    cluster_sizes[0] += 1
                    continue

                current_cluster_size = 1
                stack = [(i, j)]

                while len(stack) > 0:
                    i, j = stack.pop()
                    von_neumann_neighbours = [(i - 1, j), (i + 1, j), (i, j - 1),
                                            (i, j + 1)]

                    for i, j in von_neumann_neighbours:
                        if 0 <= i < n and 0 <= j < n:
                            if lattice[i][j] == 1 and not visited[i][j]:
                                visited[i][j] = True
                                stack.append((i, j))
                                current_cluster_size += 1
                cluster_sizes[current_cluster_size] += 1

    return cluster_sizes


def check_automaton_data():
    """ Checks how many simulation files are present in automaton_data """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(os.path.join(current_path, "automaton_data"))

    num_automaton_simulations = 0
    for file_name in files_list:
        if file_name.startswith("simulation_") and file_name.endswith(".pkl"):
            num_automaton_simulations += 1

    return num_automaton_simulations


def load_automaton_data(num_file):
    """ Loads the data from the simulation file with the given number """
    num_simulations = check_automaton_data()
    if num_file >= num_simulations:
        raise ValueError("Invalid simulation file number")

    current_path = os.path.dirname(__file__)
    file_name = os.path.join(current_path, "automaton_data",
                             "simulation_{}.pkl".format(num_file))

    with open(file_name, "rb") as file:
        return load(file)


def save_cluster_data(cluster_sizes_record, simulation_index):
    """ Saves the data of number of clusters of each size, for every year """
    current_path = os.path.dirname(__file__)
    file_name = os.path.join(current_path, "cluster_data",
                             "cluster_data_{}.pkl".format(simulation_index))

    dump(array(cluster_sizes_record, dtype=int), open(file_name, 'wb'))


if __name__ == '__main__':
    # index of the simulation whose clustering time series data must be generated
    simulation_index = int(input("Enter simulation index: "))

    lattice_record = load_automaton_data(simulation_index)
    cluster_sizes_record = []

    for i, lattice in enumerate(lattice_record):
        print("Lattice {}".format(i))
        cluster_sizes_record.append(cluster(lattice))

    save_cluster_data(cluster_sizes_record, simulation_index)

    # lattice = [
    #     [0, 0, 0, 0, 1],
    #     [0, 1, 1, 0, 0],
    #     [0, 1, 0, 1, 0],
    #     [0, 0, 1, 1, 1],
    #     [0, 0, 0, 0, 0]
    # ]

    # print(cluster(lattice))