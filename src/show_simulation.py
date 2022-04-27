from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from data_manager import load_automaton_data

def animate(i):
    im.set_array(lattice_record[i])
    return [im]

if __name__ == '__main__':
    # simulation from automaton_data that needs to be played
    simulation_index = int(input("Enter simulation index: "))
    lattice_record = load_automaton_data(simulation_index)
    num_frames = len(lattice_record)

    fig = plt.figure()
    im = plt.imshow(lattice_record[0])
    animate = FuncAnimation(fig,
                                animate,
                                frames=num_frames,
                                interval=100,
                                repeat=False)
    plt.show()