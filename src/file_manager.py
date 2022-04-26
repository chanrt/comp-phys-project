from numpy import array
from pickle import dump, load
import os

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