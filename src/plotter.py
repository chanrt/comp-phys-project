from matplotlib import pyplot as plt
from numpy import array

from linear_regression import perform_linear_regression


def rainfall_vs_forest_cover():
    """ Performing a linear fit between rainfall and forest cover, based on real-world data """
    # Result:
    # m: 0.0008587709484891738
    # c: -0.17015471066607157      
    # r_squared: 0.9399832140229544

    # This data was obtained from IKONOS satellite imaging of the Kalahari transect
    x = array([879, 811, 698, 409, 365, 216])
    y = array([0.65, 0.54, 0.32, 0.19, 0.14, 0.04])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Linear fit of Forest cover vs Rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Forest cover (fraction)")
    plt.plot(x, y, 'ko')
    x_line = array(x)
    y_line = m * x_line + c
    plt.plot(x_line, y_line)
    plt.show()


def rainfall_variation():
    """ Variation of power-law exponent with rainfall (results from automaton simulations) """
    # Result:
    # m: -0.002734285714285714
    # c: 3.165523809523809
    # r_squared: 0.9663725685022448

    # this data was obtained from the graphs under observations/rainfall_variation
    x = array([300, 400, 500, 600, 700, 800])
    y = array([2.3, 2.22, 1.74, 1.47, 1.17, 1.07])
    m, c, r_squared = perform_linear_regression(x, y)

    print(f"m: {m}")
    print(f"c: {c}")
    print(f"r_squared: {r_squared}")

    plt.title("Variation of power-law exponent with rainfall")
    plt.xlabel("Rainfall (mm/year)")
    plt.ylabel("Power-law exponent")
    plt.plot(x, y, marker="o", linestyle="None")
    y_line = m * x + c
    plt.plot(x, y_line)
    plt.show()

if __name__ == '__main__':
    rainfall_vs_forest_cover()