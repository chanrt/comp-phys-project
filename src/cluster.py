# Goes through every saved data file from automaton_data
# Generates a time series data of number of clusters of each size, for every year

from matplotlib import pyplot as plt
from numpy import zeros

from file_manager import load_automaton_data, save_cluster_data


def cluster_lattice(lattice, trim=True):
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
                    von_neumann_neighbours = [(i - 1, j), (i + 1, j),
                                              (i, j - 1), (i, j + 1)]

                    for i, j in von_neumann_neighbours:
                        if 0 <= i < n and 0 <= j < n:
                            if lattice[i][j] == 1 and not visited[i][j]:
                                visited[i][j] = True
                                stack.append((i, j))
                                current_cluster_size += 1
                cluster_sizes[current_cluster_size] += 1

    if trim:
        max_cluster_size = -1
        for i in range(n * n, 0, -1):
            if cluster_sizes[i] > 0:
                max_cluster_size = i
                break

        return cluster_sizes[:max_cluster_size + 1]
    else:
        return cluster_sizes


if __name__ == '__main__':
    # index of the simulation whose clustering time series data must be generated
    simulation_index = int(input("Enter simulation index: "))

    lattice_record = load_automaton_data(simulation_index)
    cluster_sizes_record = []

    for i, lattice in enumerate(lattice_record):
        print("Lattice {}".format(i))
        cluster_sizes_record.append(cluster_lattice(lattice))

    save_cluster_data(cluster_sizes_record, simulation_index)