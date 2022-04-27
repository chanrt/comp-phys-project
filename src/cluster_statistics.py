from math import sqrt
from numpy import mean
from cluster import cluster_lattice
from data_manager import load_automaton_data


def obtain_cluster_statistics(lattice):
    """ Given a lattice, calculates it's cluster statistics """
    cluster_data = cluster_lattice(lattice, True)
        
    num_clusters = sum(cluster_data[1:])
    size = len(lattice)
    vegetation_area = (size * size) - cluster_data[0]
    average_cluster_size = vegetation_area / num_clusters

    mean_deviation_squared_sum = 0
    for size, num_clusters_of_size in enumerate(cluster_data[1:]):
        mean_deviation_squared_sum += num_clusters_of_size * ((size - average_cluster_size)**2)
    standard_deviation = sqrt(mean_deviation_squared_sum / num_clusters)

    return num_clusters, average_cluster_size, standard_deviation


if __name__ == '__main__':
    # simulations that need to be considered
    simulation_indices = list(range(0, 5))

    num_clusters_list = []
    average_cluster_size_list = []
    sd_list = []

    for i, simulation_index in enumerate(simulation_indices):
        print(f"Lattice {i + 1} / {len(simulation_indices)} being processed")
        
        lattice_records = load_automaton_data(simulation_index)
        num_clusters, average_cluster_size, sd = obtain_cluster_statistics(lattice_records[-1])
        cluster_data = cluster_lattice(lattice_records[-1], True)

        num_clusters_list.append(num_clusters)
        average_cluster_size_list.append(average_cluster_size)
        sd_list.append(sd)

    print(f"Average number of clusters: {mean(num_clusters_list)}")
    print(f"Average cluster size: {mean(average_cluster_size_list)}")
    print(f"Standard deviation of cluster size: {mean(sd_list)}")